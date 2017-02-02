#!/usr/bin/python
# James Houston
# Prototype 1
# Pull image script

import docker
import requests
import sys
from requests import ConnectionError
from requests import ConnectTimeout

# Create docker client
client = docker.from_env()
print client
# get arguments
argLen = len(sys.argv)
if argLen < 2:
    print "Error: Invalid number of arguments. Please provide an correct image name."
    sys.exit(0)

print sys.argv
imageName = sys.argv[1]
imageTag = None
if argLen == 3:
    imageTag = sys.argv[2]

# Pull image
if imageTag:
    #try:
    pullImage = client.images.pull(imageName + ':' + imageTag)
    #except:
#	print "exception"
else:
    pullImage = client.images.pull(imageName)
    print pullImage
