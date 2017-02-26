# James Houston
# Prototype 1
# List container script

import docker
import requests
import sys
from docker import APIError
from requests import ConnectionError
from requests import ConnectTimeout

# Create docker client
client = docker.from_env()

# get arguments
#
argLen = len(sys.argv)
if argLen > 2:
    print "Error: Invalid number of arguments. \'list_containers.py <bool(listAll)>\'"
    sys.exit(0)

# list contianer
if argLen == 2:
    # List all
    allBool = sys.argv[1]
    if allBool not in ['true','True','false','False']:
        print "Error: Invalid argument passed. Second argument is of type \'bool\'"
    try:
        containerList = client.containers.list(bool(allBool))
    except APIError as e:
        print "APIError exception thrown! Exception details:"
        print '\t', e
    except ConnectTimeout as e:
        print "ConnectTimeout exception thrown! Exception details:"
        print '\t', e
    except ConnectionError as e:
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e
else:
    # List running
    containerList = client.containers.list()
