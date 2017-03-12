#!/usr/bin/python
# James Houston
# Container Orchestrator
# list_images.py

import docker
import humanize
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

def list_images(client):
    # Get the image list
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        return client.images.list()
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
    images = list_images(client)
    if images:
        count = 1
        print "Image List:", images
        print "  NAME\t\t\tSIZE"
        for image in images:
            image = image.attrs
            if len(str(image["RepoTags"][0])) <= 13:
                print str(count) + "." + str(image["RepoTags"][0]) + "\t\t" +  str(humanize.naturalsize(image["Size"]))
            else:
                print str(count) + "." + str(image["RepoTags"][0]) + "\t" +  str(humanize.naturalsize(image["Size"]))
            count += 1
    else:
        print "No images available on local system. <insert suggestion to pull image>"

if __name__ == '__main__':
    check = env_check()
    if check[1]:
        main(check[0])
