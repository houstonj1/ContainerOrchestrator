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

def main():
    # Create docker client
    client = docker.from_env()

    # Get input information -- using CLI arguments for now assuming all args are strings
    # Image name
    # Image tag (if applicable)
    # Check that minimum arguments are passed
    print sys.argv
    argLen = len(sys.argv)
    print 'length: ', argLen
    imageTag = 'latest'
    if argLen < 2:
        print "Error: Invalid number of arguments. Please provide an correct image name."
        sys.exit(0)
    elif argLen > 3:
        print "Error: Too many arguments. Please provide the correct number of arguments."
        sys.exit(0)
    else:
        imageName = sys.argv[1]
        # Check for a passed image tag
        if argLen == 3:
            imageTag = sys.argv[2]

    # Pull image
    if imageName:
        try:
            pulledImage = client.images.pull(imageName, tag=imageTag)
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
            print pulledImage
            print imageName + " image pulled successfully!"

if __name__ == '__main__':
    main()
