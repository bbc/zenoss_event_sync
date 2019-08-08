##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

import sys
import pprint
import logging
import ConfigParser

import os
import traceback
import utils

base_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_folder + '/src')
config_file = base_folder + '/src/event.config'

logger = logging.getLogger('output')
from zenoss import Zenoss, EventState, EventSeverity, ProductionState

connect_params = {'enabled': False, 'src_host': '', 'dest_host': '', 'cert': '', 'ssl_verify': False}
event_filter = {'severity': '', 'systems': '', 'prod_state': ''}

STATUS_FILE_PATH = "{}/status.json".format(base_folder)
graph_metrics = {"src_diff": 1,
                 "src_total": 1,
                 "dest_diff": 1,
                 "dest_total": 1}


# load properties
def load_properties():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(config_file)
    connect_params['enabled'] = config.getboolean('system', 'enabled')
    connect_params['test_mode'] = config.getboolean('system', 'test_mode')
    connect_params['src_host'] = config.get('connect_params', 'src_host')
    connect_params['dest_host'] = config.get('connect_params', 'dest_host')
    connect_params['username'] = config.get('connect_params', 'username')
    connect_params['password'] = config.get('connect_params', 'password')
    connect_params['cert'] = config.get('connect_params', 'cert')
    connect_params['ssl_verify'] = config.getboolean('connect_params', 'ssl_verify')
    event_filter['severity'] = config.getint('event_filter', 'severity')
    event_filter['systems'] = config.get('event_filter', 'systems')
    event_filter['prod_state'] = config.getint('event_filter', 'prod_state')
    handler = logging.FileHandler(config.get('logging', 'file'))
    formatter = logging.Formatter(config.get('logging', 'format'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(config.get('logging', 'level'))
    return True


def connection_setup(host):
    logger.info('Connecting to: {}'.format(host))
    return Zenoss(host=('%s' % host),
                  username=connect_params['username'],
                  password=connect_params['password'],
                  cert=connect_params['cert'],
                  ssl_verify=connect_params['ssl_verify'])


def get_events(zenoss, event_states, detail_format=True):
    params = {'eventState': event_states, 'prodState':  [event_filter['prod_state']], 'severity': event_filter['severity'],
              'Systems': event_filter['systems']}
    events = zenoss.get_events(limit=10000, sort='firstTime', dir='ASC', params=params, detailFormat=detail_format)
    no_of_event_state = {v: k for k, v in vars(EventState).items() if not k.startswith('__')}
    no_of_prod_state = {v: k for k, v in vars(ProductionState).items() if not k.startswith('__')}
    # logger.info('{} events retrieved: {}'.format(no_of_event_state[state], len(events)))
    logger.info(
        '{} {} events retrieved: {}'.format(', '.join([no_of_event_state[state] for state in event_states]),
                                            ', '.join([no_of_prod_state[event_filter['prod_state']]]),
                                            len(events)))
    return events


def build_event_data_structure(events):
    events_new_structure = {}
    for event in events:
        key = sanitise_dedupid(event['dedupid'])
        value = {
            'evid': event['evid'],
            'eventState': event['eventState'],
            'severity': event['severity'],
            'log': event['log']
        }
        events_new_structure.update({key: value})
    logger.debug('Event details: {}'.format(events_new_structure))
    return events_new_structure


def sanitise_dedupid(raw_dedupid):
    dedupid = raw_dedupid.split('|')
    for number, item in enumerate(dedupid):
        host = dedupid[0]+'/'
        if host in item:
            logger.info('found in [{}] : {}'.format(number, item))
            dedupid[number] = item.replace(host, '')
            return '|'.join(dedupid)
    return raw_dedupid

def compare_events(events_1, events_2, message):
    events_differences_keys = set(events_2) - set(events_1)
    logger.info('{}: {}'.format(message, len(events_differences_keys)))
    logger.debug('Events that differ detail: {}'.format(events_differences_keys))
    events_differences = {k: events_2[k] for k in events_differences_keys}
    return events_differences


def find_event_states_to_be_changed(src_events, dest_events, event_state):
    events_key_matches = set(dest_events).intersection(set(src_events))
    changeset = [dest_events[event_key]['evid'] for event_key in events_key_matches]
    logger.info('To be {}: {}'.format(event_state, len(events_key_matches)))
    logger.info('To be {}: {}'.format(event_state, events_key_matches))
    return changeset


def find_unique_events(src_events, dest_events):
    unique_events = set(src_events).difference(set(dest_events))
    return {k: v for k, v in src_events.items() if k in unique_events}


def find_event_logs_to_be_changed(src_events, dest_events):
    changeset = []
    for src_event_key, src_event_val in src_events.items():
        if src_event_key in dest_events.keys():
            src_event_logs = src_event_val['log']
            dest_event_that_matches = dest_events[src_event_key]
            new_logs = _find_new_logs_in_events(src_event_logs, dest_event_that_matches)
            changeset += new_logs
    logger.info('Log changes to Apply: {}'.format(len(changeset)))
    logger.info('Log changes to Apply: {}'.format(changeset))
    return changeset


def _find_new_logs_in_events(src_event_logs, dest_event_that_matches):
    changeset = []
    for src_event_log in src_event_logs:
        src_user, src_timestamp, src_message = src_event_log
        admin_message_1 = 'state changed to'
        admin_message_2 = 'Please refer Case'
        if any(map(lambda x: x in src_message, [admin_message_1, admin_message_2])):  # skip if admin message
            logger.debug('skipping: {}'.format(src_message))
            continue
        elif _is_log_new(src_event_log, dest_event_that_matches['log']):
            # combining src_user, src_timestamp, src_message to the dest_message field,
            # as the user and timestamp is automatically assigned to the destinations system fields
            changeset.append({dest_event_that_matches['evid']: '{}, {}, {}'.format(src_user, src_timestamp, src_message)})
    return changeset


def _is_log_new(event_log, event_logs):
    is_new = True
    for el in event_logs:
        if all([_is_message_new(el, event_log), _is_message_new(event_log, el)]):
            pass
        else:
            is_new = False
    return is_new


def _is_message_new(log1, log2):
    log1_message = log1[2]
    log2_user, log2_timestamp, log2_message = log2
    if all(map(lambda x: x in log1_message, [log2_user, str(log2_timestamp), log2_message])):
        logger.debug('--- {} {} {} is an old comment, it matches {}'.format(log1_message, log2_timestamp, log2_message,
                                                                            log1))
        return False
    return True


def close_events(evids):
    logger.info('evids: {}'.format(evids))
    return [zenoss_dest.close_event(evid) for evid in evids]


def ack_events(evids):
    result = [zenoss_dest.ack_event(evid) for evid in evids]
    if len(result):
        logger.info('Events acknowledged successfully: {}'.format(len([data for data in result if data['success']])))
        logger.debug('Events acknowledged response: {}'.format([data for data in result if data['success']]))
    return result


def new_events(evids):
    result = [zenoss_dest.change_event_state(evid, 'reopen') for evid in evids]
    if len(result):
        logger.info('Events that have changed to new successfully: {}'.format(
            len([data for data in result if data['success']])))
        logger.debug('Events that have changed to new detail : {}'.format([data for data in result if data['success']]))
    return result


def create_logs(evid_logs):
    evid_logs.reverse()  # to switch order so earliest entries get written first and latest entry last.
    for evid_log in evid_logs:
        for evid, log in evid_log.items():
            logger.info('evid: {} log: {}'.format(evid, log))
            zenoss_dest.write_log(evid, log)
    return True


def dump(events):
    print 'Dumping events'
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(events)
    print 'Dumped: {} events'.format(len(events))


def generate_metrics(event_src_diff, events_src_total, event_dest_diff, events_dest_total):
    global graph_metrics
    graph_metrics['src_diff'] = len(event_src_diff)
    graph_metrics['src_total'] = len(events_src_total)
    graph_metrics['dest_diff'] = len(event_dest_diff)
    graph_metrics['dest_total'] = len(events_dest_total)


if __name__ == "__main__":
    import datetime

    print '------------------- start -------------------------'
    print 'time: {}'.format(datetime.datetime.now())

    load_properties()
    if not connect_params['enabled']:
        sys.exit(0)

    logger.info('------------------- starting -------------------------')
    try:
        test_mode = connect_params['test_mode']
        zenoss_src = connection_setup(host=connect_params['src_host'])
        events_src_new = build_event_data_structure(get_events(zenoss_src, [EventState.new]))
        events_src_acks = build_event_data_structure(get_events(zenoss_src, [EventState.acknowledged]))
        events_src_closed = build_event_data_structure(get_events(zenoss_src, [EventState.closed]))
        events_src_new_acks = {}
        events_src_new_acks.update(events_src_new)
        events_src_new_acks.update(events_src_acks)

        zenoss_dest = connection_setup(host=connect_params['dest_host'])
        events_dest_new = build_event_data_structure(get_events(zenoss_dest, [EventState.new]))
        events_dest_acks = build_event_data_structure(get_events(zenoss_dest, [EventState.acknowledged]))
        events_dest_closed = build_event_data_structure(get_events(zenoss_dest, [EventState.closed]))
        events_dest_new_acks = {}
        events_dest_new_acks.update(events_dest_new)
        events_dest_new_acks.update(events_dest_acks)
        events_dest_acks_closed = {}
        events_dest_acks_closed.update(events_dest_acks)
        events_dest_acks_closed.update(events_dest_closed)

        event_src_differences = compare_events(events_dest_new_acks, events_src_new_acks, 'Extra events that exist on src but not on destination system')
        event_dest_differences = compare_events(events_src_new_acks, events_dest_new_acks, 'Extra events that exist on destination but not on src system')

        generate_metrics(event_src_differences, events_src_new_acks, event_dest_differences, events_dest_new_acks)

        event_ids_to_close = find_event_states_to_be_changed(events_src_closed, event_dest_differences, 'Closed')

        events_src_unique_acks = find_unique_events(events_src_acks, events_dest_acks)
        events_ids_to_ack = find_event_states_to_be_changed(events_src_unique_acks, events_dest_new, 'Acknowledged')

        events_src_unique_new = find_unique_events(events_src_new, events_dest_new)
        events_ids_to_new_from_src_new = find_event_states_to_be_changed(events_src_unique_new, events_dest_acks_closed, 'New')
        events_ids_to_new_from_src_acks = find_event_states_to_be_changed(events_src_unique_acks, events_dest_acks_closed, 'New')
        events_ids_to_new = events_ids_to_new_from_src_new + events_ids_to_new_from_src_acks
        event_logs_to_write = find_event_logs_to_be_changed(events_src_new_acks, events_dest_new_acks)

        if test_mode:
            pass
        else:  # run changes for real
            close_events(event_ids_to_close)
            ack_events(events_ids_to_ack)
            new_events(events_ids_to_new)
            create_logs(event_logs_to_write)

    except Exception as e:
        logger.info('Error Occurred: {}'.format(e.message))
        print 'Error Occurred: {}'.format(e.message)
        tb = traceback.format_exc()
        utils.add_zenoss_event(summary='Error Occurred: {}'.format(e.message), message=tb, severity=4)
        sys.exit(0)
    finally:
        utils.generate_status_file(STATUS_FILE_PATH, graph_metrics)

    logger.info('------------------- finishing  -------------------------')

    print '------------------- end -------------------------'
    print 'time: {}'.format(datetime.datetime.now())
