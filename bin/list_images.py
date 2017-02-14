#!/usr/bin/python
# James Houston
# Container Orchestrator
# list_images.py

import docker
from docker.errors import APIError
from requests import ConnectionError
from requests import ConnectTimeout

def main():
    # Create the docker client
    client = docker.from_env()

    # Get the image list
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        imageList = client.images.list()
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
        if imageList:
            print "Image List: ", imageList
            print "Image Names:"
            for image in imageList:
                print image.tags[0]
        else:
            print "No images available on local system. <insert suggestion to pull image>"

if __name__ == '__main__':
    main()
