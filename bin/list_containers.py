#!/usr/bin/python
# James Houston
# List containers script

import docker
import requests
import sys
from docker.errors import APIError
from requests import ConnectionError
from requests import ConnectTimeout

# Create docker client
client = docker.from_env()

# get arguments
argLen = len(sys.argv)
print argLen
print sys.argv
if argLen > 2:
    print "Error: Invalid number of arguments. \'list_containers.py <bool(listAll)>\'"
    sys.exit(0)

# list contianer
if argLen == 2:    # List all
    allBool = sys.argv[1]
    print allBool
    if allBool not in ['true','True','false','False']:
        print "Error: Invalid argument passed. Second argument is of type \'bool\'"
    else:
        allBool = bool(allBool)
        try:
            containerList = client.containers.list(allBool)
        except APIError as e:
            print "APIError exception thrown! Exception details:"
            print '\t', e
        except ConnectTimeout as e:
            print "ConnectTimeout exception thrown! Exception details:"
            print '\t', e
        except ConnectionError as e:
            print "ConnectionError exception thrown! Exception details:"
            print '\t', e
else:    # List running
    try:
        containerList = client.containers.list()
    except APIError as e:
        print "APIError exception thrown! Exception details:"
        print '\t', e
    except ConnectTimeout as e:
        print "ConnectTimeout exception thrown! Exception details:"
        print '\t', e
    except ConnectionError as e:
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e

# Print contianer information
print containerList
for container in containerList:
    shortId = container.short_id
    name = container.name
    status = container.status
    print "Name:", name, "Short ID:", shortId, "Status:", status
