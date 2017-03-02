#!/usr/bin/python
# James Houston
# Container Orchestrator
# remove_image.py

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

def remove_image(client,image):
    # Remove an image
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        client.images.remove(image)
        return str(image) + " removed successfully."
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
    if argLen > 2:
        print "Error: Invalid arguments. ./remove_image image"
        sys.exit(0)
    else:
        imageName = sys.argv[1]
        print remove_image(client,imageName)

if __name__ == '__main__':
    check = env_check()
    if check[1]:
        main(check[0])
