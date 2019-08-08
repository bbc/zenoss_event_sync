##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

import json
import time
import logging

logger = logging.getLogger(__name__)

zenoss_events = []


def add_zenoss_event(summary, message, severity):
    logger.debug("summary '{}'".format(summary))
    global zenoss_events
    zenoss_events.append({
        "severity": severity,
        "component": "zenoss-event-sync",
        "summary": summary,
        "message": message
    })


def generate_status_file(filepath, values):
    logger.info("filepath '{}'".format(filepath))
    values["last_updated_timestamp"] = int(time.time())
    empty_component = ""
    status ={"values": {empty_component: values},
             "events": zenoss_events}
    with open(filepath, 'w') as f:
        json.dump(status, f)
