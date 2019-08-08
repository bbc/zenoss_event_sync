# zenoss_sync
Keeps two separate Zenoss event consoles in sync and provides information on the sync level achieved.
In addition you can report on the Zenoss collector device totals, device differences and device uniqueness
between two seperate Zenoss systems.

This project is licensed under the terms of the Apache license 2.0.

## Background:

This software primarily tries to solve the issue of keeping a failover system's event console up to date.
Through configuration you can choose which event types you'd like to keep in sync.
It also provides some reporting and information on the device and sync levels.

- Currently the event parts that that are replicated are:
    - EventState: New, Ack'd and Closed
    - Event Log comments (comments that are manually appended to events)

How the events are compared:
- The software uses the dedupid to compare events from one system to the other e.g. router1.example.com|FastEthernet0/1|/Perf/Interface|threshName. This is a system independant way to make comparisons of the same event on an entirely
different zenoss installation. Normally this feature is used to increase a counter field (to an existing event to show it has repeated a number of times on the same system).

The software interacts with running Zenoss installations by using the Zenoss API of each separately running Zenoss RM.
- There are a number of pre-reqs for the zenoss setup:
    - Devices and templates on both systems are the same. (achieved through Zenoss config manager or by scripting  ZenDMD or also the API.)
    - Two Zenoss 5 or 6 installs (tested on)
    - You have Resource manager event consoles running on two seperate Zenoss systems one acting as say a primary and the other as failover (secondary)
    - Use Cron to execute event.py using flock.
    
            
    */1 * * * * flock -xn /home/servim/event.lck -c /home/servim/zenoss_event_sync/src/event_sync.sh >> /var/log/event_sync.log 2>&1


## Prereqs:

    - Python 2.7x
    - pip install requests
    - pip install zenoss-fork 

## Installation - software is setup up as follows:

    - Git clone the repo
    - Copy your cert/key (cert and key in one file in that order) 
      over to connect to the API or use username/password 
    - Adjust the config below for your endpoints (rmhosts) and events you are interested in keeping in sync
    - Run on a cron - use flock or similar to allow each run to complete before the next iteration starts (e.g 1 min    cycles)
      */1 * * * * flock -xn /home/servim/event.lck -c /opt/zenoss_event_sync/src/event_sync.sh >> /var/log
      /event_sync.log 2>&1
          
## Config:
     -src/event.example_config (rename by removing 'example_' e.g. event.config)
     -src/device_status.example_config (rename by removing 'example_' e.g. device_status.config) 
     

## Logging:
- Extensive logging about what was sync'd and time things took:
- log src/event.log
- Also you can allow zenoss-fork to also use the same logger change zenoss.py (start of file):
    
    
    -logging.getLogger(__name__) to logging.getLogger('output')  
    
    
## Reporting:
- status.json is created and this can be graphed - choose nagios parser.
- devices.py and  there is a device and collector report which gives comprehensive information about the number of
devices and their production state on each collector and total between the instances - to help keep a track.
- devices_status.py and their production state


## Deploy to live:

- edit event.config add config, watch out for full path to event.log
- host you want to sync
- username/password or cert
- full path (on live) to event.log
- log level
- set event filter severity and tags, otherwise nothing will get picked up
    
## Troubleshooting:

- Error Occurred: HTTPSConnectionPool(host='zenoss-a', port=443): Max retries exceeded with url: /zport/dmd/evconsole_router (Caused by SSLError(SSLError(336445449, u'[SSL] PEM lib (_ssl.c:2780)'),))
    - usually a incorrect cert/key combo
- HTTP 400 error
    - Username/password is not working or URL's to zenoss RM's are not correct.
- Other issues please look at the src/event.log


## Testing

- unittests with arguments python -m unittest discover -s <fullpath>/zenoss_event_sync/test -p test_event_sync.py -t <fullpath>/zenoss_event_sync/test in <fullpath>/zenoss_event_sync/test


## Linting

Please make sure that all code is linted before it is committed to the repo



## Development

Please raise pull requests with changes in rather than committing directly to Master.


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

Please ensure you have run the test suite before submitting a Pull Request, and include a version bump in line with our [Versioning](#versioning) policy.

## License

See [LICENSE.md](LICENSE.md)

This is licensed under the Apache 2.0 License.

## Copyright

Copyright (c) 2018 BBC

