#!/usr/bin/python
# James Houston
# Container Orchestrator
# remove_container.py

import docker
import requests
import sys
from docker.errors import ContainerError
from docker.errors import ImageNotFound
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

def create_container(client, imageName, command=None, detach=True, hostname=None, name=None, networkDisabled=True, networkMode=none, ports={}):
    # Create a container
    # Throws docker.errors.ContainerError if container exits with a non-zero exit code and detach is False
    # Throws docker.errors.ImageNotFound if the specified image does not exist
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        return client.containers.create(imageName, command=command, detach=detach, hostname=hostanme, name=name, network_disabled=networkDisabled, network_mode=networkMode, ports=ports)
    except ContainerError as e:
        # This is important
        print "ContainerError exception thrown! Exception details:"
        print '\t', e
    except ImageNotFound as e:
        # This is important
        print "ImageNotFound exception thrown! Exception details:"
        print '\t', e
    except APIError as e:
        print "APIError exception thrown! Exception details:"
        print '\t', e
    except ConnectTimeout as e:
        print "ConnectTimeout exception thrown! Exception details:"
        print '\t', e
    except ConnectionError as e:
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e
