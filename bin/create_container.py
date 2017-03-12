#!/usr/bin/python
# James Houston
# Container Orchestrator
# remove_container.py

import docker
import json
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

def create_container(client,imageName,command,detach,hostname,name,networkDisabled,networkMode,macAddr,ports,publishPorts):
    # Create a container
    # Throws docker.errors.ContainerError if container exits with a non-zero exit code and detach is False
    # Throws docker.errors.ImageNotFound if the specified image does not exist
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        return client.containers.create(imageName,command,detach=detach,hostname=hostname,name=name,network_disabled=networkDisabled,network_mode=networkMode,mac_address=macAddr,ports=ports,publish_all_ports=publishPorts)
    except ContainerError as e:
        # This is important
        print "ContainerError exception thrown! Exception details:"
        print '\t', e
    except ImageNotFound as e:
        # This is important
        print "ImageNotFound exception thrown! Exception details:"
        print '\t', e
    except APIError as e:
        # Error 409 exception for network mode and mac address -- needs to be bridge to set a mac
        print "APIError exception thrown! Exception details:"
        print '\t', e
    except ConnectTimeout as e:
        print "ConnectTimeout exception thrown! Exception details:"
        print '\t', e
    except ConnectionError as e:
        print "ConnectionError exception thrown! Exception details:"
        print '\t', e

def main(client):
    # get  arguments
    argLen = len(sys.argv)
    # Check for required args
    if argLen < 2:
        print "Error: Invalid arguments."
        print "./create_container.py imageName command detach hostname name networkDisabled networkMode macAddress ports publishPorts"
        sys.exit(0)
    elif argLen >= 2:
        imageName = sys.argv[1]
        command = sys.argv[2]
        detach = bool(sys.argv[3])
        hostname = sys.argv[4]
        name = sys.argv[5]
        networkOn = bool(sys.argv[6])
        netMode = sys.argv[7]
        mac = sys.argv[8]
        ports = json.loads(sys.argv[9])
        pubPorts = bool(sys.argv[10])
        print create_container(client,imageName,command,detach,hostname,name,networkOn,netMode,mac,ports,pubPorts)
    else:
        print "Error: Invalid arguments."
        print "./create_container.py imageName command detach hostname name networkDisabled networkMode macAddress ports publishPorts"
        sys.exit(0)

if __name__ == '__main__':
    check = env_check()
    if check[1]:
        main(check[0])
