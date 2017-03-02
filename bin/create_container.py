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

def create_container(client, imageName, command="", detach=True, hostname="",
                     name="", networkDisabled=True, networkMode="host", ports={}, publish_all_ports=True):
    # Create a container
    # Throws docker.errors.ContainerError if container exits with a non-zero exit code and detach is False
    # Throws docker.errors.ImageNotFound if the specified image does not exist
    # Throws docker.errors.APIError if server returns an error
    # Throws requests.ConnectTimeout if the http request to docker times out
    # Throws requests.ConnectionError if the docker daemon is unreachable
    try:
        return client.containers.create(imageName, command=command, detach=detach,
                                        hostname=hostname, name=name, network_disabled=networkDisabled,
                                        network_mode=networkMode, ports=ports, publish_all_ports=publish_all_ports)
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

def main(client):
    # get  arguments
    argLen = len(sys.argv)
    # Check for required args
    if argLen < 2:
        print "Error: Invalid arguments. ./create_container.py imageName name detach=True command=\"\" ports=\{\}"
        sys.exit(0)
    elif argLen == 2:
        imageName = sys.argv[1]
        print create_container(client,imageName)
    elif argLen == 3:
        imageName = sys.argv[1]
        name = sys.argv[2]
        print create_container(client,imageName,name=name)
    elif argLen == 4:
        imageName = sys.argv[1]
        name = sys.argv[2]
        detach = sys.argv[3]
        print create_container(client,imageName,name=name,detach=detach)
    elif argLen == 5:
        imageName = sys.argv[1]
        name = sys.argv[2]
        detach = sys.argv[3]
        command = sys.argv[4]
        print create_container(client,imageName,name=name,detach=detach,command=command)
    elif argLen == 7:
        imageName = sys.argv[1]
        name = sys.argv[2]
        detach = sys.argv[3]
        command = sys.argv[4]
        port1 = sys.argv[5]
        port2 = sys.argv[6]
        if port2 == "None":
            port2 = None
        ports = {port1:int(port2)}
        print ports
        print type(ports)
        print create_container(client,imageName,name=name,detach=detach,command=command,ports=ports)
    else:
        print "Error: Invalid arguments. ./create_container.py imageName name detach=True command=\"\" ports=\{\}"
        sys.exit(0)

if __name__ == '__main__':
    check = env_check()
    if check[1] == True:
        main(check[0])
