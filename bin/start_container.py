#!/usr/bin/python
# James Houston
# Container Orchestrator
# start_container.py

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

def start_container(client, containerName):
    # Start a container
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        container = client.containers.get(containerName)
        container.start()
        return containerName + " started successfully."
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
    if  argLen < 2:
        print "Error: Invalid arguments. ./remove_container containerName volBool=True force=False"
        sys.exit(0)
    else:
        containerName = sys.argv[1]
        print start_container(client,containerName)

if __name__ == '__main__':
    check = env_check()
    if check[1]:
        main(check[0])
