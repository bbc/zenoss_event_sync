##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

import requests
import logging
import pprint

logger = logging.getLogger(__name__)


def add_note_to_alert(note, alert_id, alerta_api_url):
    body = {
      "note": note 
    }
    alerta_note_api_url = "{}/{}/note".format(alerta_api_url, alert_id)
    response = requests.put(alerta_api_url, json=body)


def send_event_to_alerta(event, alerta_api_url):
    SEVERITIES = ["cleared" ,"debug" ,"trace" ,"warning" ,"major" ,"critical"]
    STATUS = {"New": "open" ,"Acknowledged": "ack" , "Closed": "closed"}
    environment = "Development"

    body = {
      "resource": event['device'],
      "event": event['dedupid'],
      "environment": environment,
      "severity": SEVERITIES[event['severity']],
      "status": STATUS[event['eventState']],
      "correlate": [],
      "service": [
	event['component']
      ],
      "group": "Zenoss",
      "value": event['summary'],
      "text": event['message'],
      "tags": [system['name'] for system in event['Systems']],
      "attributes": {},
      "origin": "zenoss_event_sync",
      "type": "zenoss_event"
    }
    response = requests.post(alerta_api_url, json=body)

    if response.status_code != 201:
        logger.error("request to alerta failed {}".format(response.text))

    #pprint.pprint(response.json())
    # TODO sync log entries?

