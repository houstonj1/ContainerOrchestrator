#!/usr/bin/python
# James Houston
# Container Orchestrator
# remove_container.py

import docker
import requests
import sys
from docker.errors import APIError
from requests import ConnectionError
from requests import ConnectTimeout

def env_check():
    # Create the docker client
    client = docker.from_env()
    # Try to ping to ensure it is working
    try:
        retVal = client.ping()
        return client,retVal
    except ConnectionError as e:
        # Docker service is down....
        # Try to bring back up?
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e
        return client,False

def remove_container(client, containerName, volBool = True, force = False):
    # Remove a container
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        container = client.containers.get(containerName)
        container.remove(v=volBool,force=force)
        return containerName + " removed successfully."
    except APIError as e:
        print "APIError exception thrown! Exception details:"
        print '\t', e
    except ConnectTimeout as e:
        print "ConnectTimeout exception thrown! Exception details:"
        print '\t', e
    except ConnectionError as e:
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e

def main(client):
    # get arguments
    argLen = len(sys.argv)
    boolList = ['true','True','false','False']
    if not 2 <= argLen <= 4:
        print "Error: Invalid arguments. ./remove_container containerName volBool=True force=False"
        sys.exit(0)
    else:
        containerName = sys.argv[1]
        if argLen == 2:
            print remove_container(client, containerName)
        elif argLen == 3:
            volBool = sys.argv[2]
            if volBool not in boolList:
                print "Error: Invalid argument. volBool and force arguments must be True or False"
                sys.exit(0)
            else:
                volBool = bool(volBool)
                print remove_container(client, containerName, volBool)
        else:
            volBool = sys.argv[2]
            force = sys.argv[3]
            if volBool not in boolList or force not in boolList:
                print "Error: Invalid argument. volBool and force arguments must be True or False"
                sys.exit(0)
            else:
                volBool = bool(volBool)
                force = bool(force)
                print remove_container(client, containerName, volBool, force)

if __name__ == '__main__':
    check = env_check()
    if check[1]:
        main(check[0])
