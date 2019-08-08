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
config_file = base_folder + '/src/device.config'

logger = logging.getLogger('output')
from zenoss import Zenoss

connect_params = {'enabled': False, 'src_host': '', 'dest_host': '', 'cert': '', 'ssl_verify': False}
event_filter = {'severity': '', 'systems': '', 'prod_state': ''}

STATUS_FILE_PATH = "{}/devicestatus.json".format(base_folder)
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


def build_device_data_structure(devices):
    device_new_structure = {}
    for device in devices['devices']:
        key = device['name']
        value = {
            u'productionState': device['productionState'],
            u'ipAddressString': device['ipAddressString'],
            u'collector': device['collector']
        }
        device_new_structure.update({key: value})
    logger.debug('Device details: {}'.format(device_new_structure))
    return device_new_structure


def find_unique_devices(src_devices, dest_devices):
    unique_devices = set(dest_devices).difference(set(src_devices))
    return {k: v for k, v in dest_devices.items() if k in unique_devices}


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
        src_devices = build_device_data_structure(Zenoss.get_devices(zenoss_src))

        zenoss_dest = connection_setup(host=connect_params['dest_host'])
        dest_devices = build_device_data_structure(Zenoss.get_devices(zenoss_dest))

        unique_dest_devices = find_unique_devices(src_devices, dest_devices)

        if test_mode:
            print 'Test Decommissioning {} devices from {}'.format(len(unique_dest_devices), 'destination')
            for device in set(unique_dest_devices):
                if unique_dest_devices['device']['productionState'] == -1:
                    print 'Test Will be Decommissioning: {}'.format(device)
        else:  # run changes for real
            print 'Decommissioning {} devices from {}'.format(len(unique_dest_devices), 'destination')
            for device in set(unique_dest_devices):
                if unique_dest_devices[device]['productionState'] != -1:
                    print 'Decommissioning: {}'.format(device)
                    # Zenoss.set_prod_state(zenoss_dest, device, -1)
                else:
                    print 'Already Decommissioned: {} skipping...'.format(device)

    except Exception as e:
        logger.info('Error Occurred: {}'.format(e.message))
        print 'Error Occurrd: {}'.format(e.message)
        tb = traceback.format_exc()
        utils.add_zenoss_event(summary='Error Occurred: {}'.format(e.message), message=tb, severity=4)
        sys.exit(0)
    finally:
        utils.generate_status_file(STATUS_FILE_PATH, graph_metrics)

    logger.info('------------------- finishing  -------------------------')

    print '------------------- end -------------------------'
    print 'time: {}'.format(datetime.datetime.now())
