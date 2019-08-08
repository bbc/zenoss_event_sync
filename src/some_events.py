##############################################################################
#
# Copyright (C) BBC 2018
#
##############################################################################

events = [
    {
        "prodState": "Maintenance",
        "firstTime": 1494707632.238,
        "device_uuid": "3cb330f3-afb0-4e25-99ef-1902403b9be1",
        "eventClassKey": null,
        "severity": 5,
        "agent": "zenperfsnmp",
        "dedupid": "rpm01.rbsov.bbc.co.uk||/Status/Snmp|snmp_error|5",
        "Location": [
            {
                "uid": "/zport/dmd/Locations/RBSOV",
                "name": "/RBSOV"
            }
        ],
        "component_url": null,
        "ownerid": null,
        "eventClassMapping_url": null,
        "eventClass": "/Status/Snmp",
        "eventState": "New",
        "id": "0242ac11-0008-8c73-11e7-381b7d3bc1c5",
        "device_title": "rpm01.rbsov.bbc.co.uk",
        "DevicePriority": null,
        "log": [
            [
                "admin",
                "2017-05-17 05:14:39",
                "Please refer Case3 <a href=\"https://confluence.dev.bbc.co.uk/display/men/Auto+Closing+and+Unacknowledging+events+in+zenoss\"><b> here</b> </a>"
            ],
            [
                "admin",
                "2017-05-17 05:14:39",
                "state changed to New"
            ],
            [
                "syed.rafiq@bbc.co.uk",
                "2017-05-13 23:02:06",
                "state changed to Acknowledged"
            ]
        ],
        "facility": null,
        "eventClass_url": "/zport/dmd/Events/Status/Snmp",
        "priority": null,
        "device_url": "/zport/dmd/goto?guid=3cb330f3-afb0-4e25-99ef-1902403b9be1",
        "DeviceClass": [
            {
                "uid": "/zport/dmd/Devices/Network/RPM Probes",
                "name": "/Network/RPM Probes"
            }
        ],
        "details": [
            {
                "value": "a72e9aea2240",
                "key": "manager"
            },
            {
                "value": "/Network/RPM Probes",
                "key": "zenoss.device.device_class"
            },
            {
                "value": "/Platform/Network Equipment/Routers_Firewalls",
                "key": "zenoss.device.groups"
            },
            {
                "value": "172.31.193.90",
                "key": "zenoss.device.ip_address"
            },
            {
                "value": "/RBSOV",
                "key": "zenoss.device.location"
            },
            {
                "value": "300",
                "key": "zenoss.device.production_state"
            },
            {
                "value": "/ReleaseEnvironment/Live",
                "key": "zenoss.device.systems"
            }
        ],
        "evid": "0242ac11-0008-8c73-11e7-381b7d3bc1c5",
        "component_uuid": null,
        "eventClassMapping": null,
        "component": null,
        "clearid": null,
        "DeviceGroups": [
            {
                "uid": "/zport/dmd/Groups/Platform/Network Equipment/Routers_Firewalls",
                "name": "/Platform/Network Equipment/Routers_Firewalls"
            }
        ],
        "eventGroup": "SnmpTest",
        "device": "rpm01.rbsov.bbc.co.uk",
        "component_title": null,
        "monitor": "TELHC-Collector",
        "count": 13361,
        "stateChange": 1494998079.655,
        "ntevid": null,
        "summary": "Cannot connect to SNMP agent on rpm01.rbsov.bbc.co.uk: Session.get: snmp_send cliberr=0, snmperr=-27, errstring=No securityName specified",
        "message": "Cannot connect to SNMP agent on rpm01.rbsov.bbc.co.uk: Session.get: snmp_send cliberr=0, snmperr=-27, errstring=No securityName specified<br/><a href=\"https://confluence.dev.bbc.co.uk/label/zenoss_evtclass_status_snmp\"><b> Event Class Run Book</b> </a><br/><b>Confluence Label</b>: <i>zenoss_evtclass_status_snmp</i>",
        "eventKey": "snmp_error",
        "lastTime": 1498735871.863,
        "ipAddress": [
            "172.31.193.90"
        ],
        "Systems": [
            {
                "uid": "/zport/dmd/Systems/ReleaseEnvironment/Live",
                "name": "/ReleaseEnvironment/Live"
            }
        ]
    },
    {
        "prodState": "Maintenance",
        "firstTime": 1494707633.109,
        "device_uuid": "61266bba-2a7d-4551-a778-22171ffec006",
        "eventClassKey": null,
        "severity": 5,
        "agent": "zenping",
        "dedupid": "g7-0-sas2.oob.cwwtf.local||/Status/Ping|5|g7-0-sas2.oob.cwwtf.local is DOWN!",
        "Location": [
            {
                "uid": "/zport/dmd/Locations/Watford/Rack_G7",
                "name": "/Watford/Rack_G7"
            }
        ],
        "component_url": null,
        "ownerid": null,
        "eventClassMapping_url": null,
        "eventClass": "/Status/Ping",
        "eventState": "New",
        "id": "0242ac11-0008-8c73-11e7-381b7b7a148e",
        "device_title": "g7-0-sas2.oob.cwwtf.local",
        "DevicePriority": "Normal",
        "log": [],
        "facility": null,
        "eventClass_url": "/zport/dmd/Events/Status/Ping",
        "priority": null,
        "device_url": "/zport/dmd/goto?guid=61266bba-2a7d-4551-a778-22171ffec006",
        "DeviceClass": [
            {
                "uid": "/zport/dmd/Devices/Storage/HP/Switches",
                "name": "/Storage/HP/Switches"
            }
        ],
        "details": [
            {
                "value": "True",
                "key": "isManageIp"
            },
            {
                "value": "65e386ce4c65",
                "key": "manager"
            },
            {
                "value": "/Storage/HP/Switches",
                "key": "zenoss.device.device_class"
            },
            {
                "value": "172.31.127.128",
                "key": "zenoss.device.ip_address"
            },
            {
                "value": "/Watford/Rack_G7",
                "key": "zenoss.device.location"
            },
            {
                "value": "3",
                "key": "zenoss.device.priority"
            },
            {
                "value": "300",
                "key": "zenoss.device.production_state"
            },
            {
                "value": "/Infrastructure/Storage",
                "key": "zenoss.device.systems"
            },
            {
                "value": "/Platform/Forge/Live",
                "key": "zenoss.device.systems"
            },
            {
                "value": "/ReleaseEnvironment/Live",
                "key": "zenoss.device.systems"
            }
        ],
        "evid": "0242ac11-0008-8c73-11e7-381b7b7a148e",
        "component_uuid": null,
        "eventClassMapping": null,
        "component": null,
        "clearid": null,
        "DeviceGroups": [],
        "eventGroup": "Ping",
        "device": "g7-0-sas2.oob.cwwtf.local",
        "component_title": null,
        "monitor": "CWWTF-Collector",
        "count": 33388,
        "stateChange": 1494707633.109,
        "ntevid": null,
        "summary": "g7-0-sas2.oob.cwwtf.local is DOWN!",
        "message": "g7-0-sas2.oob.cwwtf.local is DOWN!<br/><a href=\"https://confluence.dev.bbc.co.uk/label/zenoss_evtclass_status_ping\"><b> Event Class Run Book</b> </a><br/><b>Confluence Label</b>: <i>zenoss_evtclass_status_ping</i>",
        "eventKey": "",
        "lastTime": 1498736083.126,
        "ipAddress": [
            "172.31.127.128"
        ],
        "Systems": [
            {
                "uid": "/zport/dmd/Systems/Infrastructure/Storage",
                "name": "/Infrastructure/Storage"
            },
            {
                "uid": "/zport/dmd/Systems/Platform/Forge/Live",
                "name": "/Platform/Forge/Live"
            },
            {
                "uid": "/zport/dmd/Systems/ReleaseEnvironment/Live",
                "name": "/ReleaseEnvironment/Live"
            }
        ]
    },
    {
        "prodState": "Maintenance",
        "firstTime": 1494707633.11,
        "device_uuid": "2f454a17-ce6d-4138-8609-86eab9ab4d44",
        "eventClassKey": null,
        "severity": 5,
        "agent": "zenping",
        "dedupid": "g9-0-sas2.oob.cwwtf.local||/Status/Ping|5|g9-0-sas2.oob.cwwtf.local is DOWN!",
        "Location": [
            {
                "uid": "/zport/dmd/Locations/Watford/Rack_G9",
                "name": "/Watford/Rack_G9"
            }
        ],
        "component_url": null,
        "ownerid": null,
        "eventClassMapping_url": null,
        "eventClass": "/Status/Ping",
        "eventState": "New",
        "id": "0242ac11-0008-8c73-11e7-381b7b7ab0d1",
        "device_title": "g9-0-sas2.oob.cwwtf.local",
        "DevicePriority": "Normal",
        "log": [],
        "facility": null,
        "eventClass_url": "/zport/dmd/Events/Status/Ping",
        "priority": null,
        "device_url": "/zport/dmd/goto?guid=2f454a17-ce6d-4138-8609-86eab9ab4d44",
        "DeviceClass": [
            {
                "uid": "/zport/dmd/Devices/Storage/HP/Switches",
                "name": "/Storage/HP/Switches"
            }
        ],
        "details": [
            {
                "value": "True",
                "key": "isManageIp"
            },
            {
                "value": "65e386ce4c65",
                "key": "manager"
            },
            {
                "value": "/Storage/HP/Switches",
                "key": "zenoss.device.device_class"
            },
            {
                "value": "172.31.127.132",
                "key": "zenoss.device.ip_address"
            },
            {
                "value": "/Watford/Rack_G9",
                "key": "zenoss.device.location"
            },
            {
                "value": "3",
                "key": "zenoss.device.priority"
            },
            {
                "value": "300",
                "key": "zenoss.device.production_state"
            },
            {
                "value": "/Infrastructure/Storage",
                "key": "zenoss.device.systems"
            },
            {
                "value": "/Platform/Forge/Live",
                "key": "zenoss.device.systems"
            },
            {
                "value": "/ReleaseEnvironment/Live",
                "key": "zenoss.device.systems"
            }
        ],
        "evid": "0242ac11-0008-8c73-11e7-381b7b7ab0d1",
        "component_uuid": null,
        "eventClassMapping": null,
        "component": null,
        "clearid": null,
        "DeviceGroups": [],
        "eventGroup": "Ping",
        "device": "g9-0-sas2.oob.cwwtf.local",
        "component_title": null,
        "monitor": "CWWTF-Collector",
        "count": 33389,
        "stateChange": 1494707633.11,
        "ntevid": null,
        "summary": "g9-0-sas2.oob.cwwtf.local is DOWN!",
        "message": "g9-0-sas2.oob.cwwtf.local is DOWN!<br/><a href=\"https://confluence.dev.bbc.co.uk/label/zenoss_evtclass_status_ping\"><b> Event Class Run Book</b> </a><br/><b>Confluence Label</b>: <i>zenoss_evtclass_status_ping</i>",
        "eventKey": "",
        "lastTime": 1498736083.125,
        "ipAddress": [
            "172.31.127.132"
        ],
        "Systems": [
            {
                "uid": "/zport/dmd/Systems/Infrastructure/Storage",
                "name": "/Infrastructure/Storage"
            },
            {
                "uid": "/zport/dmd/Systems/Platform/Forge/Live",
                "name": "/Platform/Forge/Live"
            },
            {
                "uid": "/zport/dmd/Systems/ReleaseEnvironment/Live",
                "name": "/ReleaseEnvironment/Live"
            }
        ]
    }

    ]