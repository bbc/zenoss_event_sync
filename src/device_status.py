##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

import sys
# import pprint
import logging
import ConfigParser

import os
import utils

import traceback

base_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_folder + '/src')
config_file = base_folder + '/src/device_status.config'

logger = logging.getLogger('output')
from zenoss import Zenoss, EventState, EventSeverity, ProductionState

prod_states = {
    str(ProductionState().production): 'production',
    str(ProductionState().pre_production): 'pre_production',
    str(ProductionState().test): 'test',
    str(ProductionState().maintenance): 'maintenance',
    str(ProductionState().decommissioned): 'decommissioned'
}

connect_params = {'enabled': False, 'src_host': '', 'dest_host': '', 'cert': '', 'ssl_verify': False}
event_filter = {'severity': '', 'systems': '', 'prod_state': ''}
devices_to_ignore = []

STATUS_FILE_PATH = "{}/device_status.json".format(base_folder)
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
    devices_to_ignore.extend(config.get('devices', 'ignore').split(' '))
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


def get_production_state(prod_code):
    return prod_states[str(prod_code)]


def extract_device_class_from_uid(uid):
    return uid[len('/zport/dmd/Devices'):uid.rfind('/devices' )]


def build_device_data_structure(devices):
    device_new_structure = {}
    for device in devices['devices']:
        key = device['name']
        value = {
            u'deviceClass': extract_device_class_from_uid(device['uid']),
            u'productionState': get_production_state(device['productionState']),
            u'ipAddressString': device['ipAddressString'],
            u'collector': device['collector']
        }
        device_new_structure.update({key: value})
    logger.debug('Device details: {}'.format(device_new_structure))
    return device_new_structure


def find_unique_devices(src_devices, dest_devices):
    unique_devices_on_src_keys = set(src_devices).difference(set(dest_devices))
    unique_devices_on_dest_keys = set(dest_devices).difference(set(src_devices))
    unique_devices_on_src = {k: v for k, v in src_devices.items() if k in unique_devices_on_src_keys}
    unique_devices_on_dest = {k: v for k, v in dest_devices.items() if k in unique_devices_on_dest_keys}
    return unique_devices_on_src, unique_devices_on_dest


def find_collector_device_totals(src_devices):
    collector_totals = {}
    for device, value in src_devices.items():
        if value['collector'] in collector_totals:
            collector_totals[value['collector']] = collector_totals[value['collector']] + 1
        else:
            collector_totals[value['collector']] = 1
    return collector_totals


def line_separate(width):
    print '-' * width


def remove_ignored_devices(unique_devices, ignored_devices):
    for unique_device in set(unique_devices):
        if unique_device.lower() in ignored_devices:
            del unique_devices[unique_device]

if __name__ == "__main__":
    import datetime
    start_time = datetime.datetime.now()

    load_properties()
    if not connect_params['enabled']:
        sys.exit(0)

    logger.info('------------------- starting -------------------------')
    try:
        test_mode = connect_params['test_mode']
        zenoss_src = connection_setup(host=connect_params['src_host'])
        src_devices = build_device_data_structure(Zenoss.get_devices(zenoss_src))

        zenoss_dest = connection_setup(host=connect_params['dest_host'])
        dest_devices = build_device_data_structure(Zenoss.get_devices(zenoss_dest))

        src_unique_devices, dest_unique_devices = find_unique_devices(src_devices, dest_devices)

        # now remove systems to be ignore
        remove_ignored_devices(src_unique_devices, devices_to_ignore)
        remove_ignored_devices(dest_unique_devices, devices_to_ignore)

        src_collector_totals = find_collector_device_totals(src_devices)
        dest_collector_totals = find_collector_device_totals(dest_devices)

        width = 50
        if test_mode:
            sys.exit(0)
        else:  # run changes for real
            line_separate(width)
            print 'Report for Zenoss collector device totals and device differences on primary and secondary systems'
            print 'Comparing Primary: {} Vs Secondary: {}'.format(connect_params['src_host'], connect_params['dest_host'])
            line_separate(width)
            print ''
            line_separate(width)
            print 'Total Devices on Zenoss primary and secondary:'
            line_separate(width)
            print 'Total Devices on Zenoss Primary: {}'.format(len(src_devices))
            print 'Total Devices on Zenoss Secondary: {}'.format(len(dest_devices))
            print ''
            line_separate(width)
            print 'Collector device Totals (Primary / Secondary):'
            line_separate(width)
            for src_collector_name, src_collector_totals in src_collector_totals.items():
                print 'Name: {} Total_Devices: {} / {}'.format(src_collector_name, src_collector_totals, dest_collector_totals.get(src_collector_name, 0))
            print ''
            line_separate(width)
            print 'On Zenoss {} there are {} unique devices:'.format('Primary', len(src_unique_devices))
            line_separate(width)
            for device in sorted(src_unique_devices.iterkeys()):
                print '{}\t {}\t {}'.format(device, src_unique_devices[device]['productionState'], src_unique_devices[device]['deviceClass'])
            print ''
            line_separate(width)
            print 'On Zenoss {} there are {} unique devices:'.format('Secondary', len(dest_unique_devices))
            line_separate(width)
            for device in sorted(dest_unique_devices.iterkeys()):
                print '{}\t {}\t {}'.format(device, dest_unique_devices[device]['productionState'], dest_unique_devices[device]['deviceClass'])
            print ''
            line_separate(width)
            print 'If you wanted to delete any unique devices please follow the below guide:'
            line_separate(width)
            print 'https://<wiki_host>/display/mon/Device+and+Collector+status+for+Zenoss+Primary+and+Secondary'
            print ''

    except Exception as e:
        logger.info('Error Occurred: {}'.format(e.message))
        print 'Error Occurred: {}'.format(traceback.format_exc())
        tb = traceback.format_exc()
        utils.add_zenoss_event(summary='Error Occurred: {}'.format(e.message), message=tb, severity=4)
        sys.exit(0)
    finally:
        utils.generate_status_file(STATUS_FILE_PATH, graph_metrics)

    logger.info('------------------- finishing  -------------------------')
    line_separate(width)
    print 'Time to run:'
    line_separate(width)
    print 'start_time: {}'.format(start_time)
    print 'end_time: {}'.format(datetime.datetime.now())