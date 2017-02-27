#!/usr/bin/python
# James Houston
# Container Orchestrator
# pull_image.py

import docker
import requests
import sys
import timeit
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

def pull_image(client,name,tag = "latest"):
    try:
        return client.images.pull(name, tag=tag)
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
    if not 2 <= argLen <= 3:
        print "Error: Invalid arguments. ./pull_image imageName tag"
        sys.exit(0)
    else:
        imageName = sys.argv[1]
        # Check for a passed image tag
        if argLen == 3:
            imageTag = sys.argv[2]
            print pull_image(client, imageName, imageTag)
        else:
            print pull_image(client,imageName)


if __name__ == '__main__':
    check = env_check()
    if check[1] == True:
        main(check[0])
