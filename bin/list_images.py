# James Houston
# Initial list images testing

import docker
import requests
from requests import ConnectionError
from requests import ConnectTimeout

# Create docker client
client = docker.from_env()

# List images
try:
    imageList = client.images.list()
# Handle exceptions -- log error and recover
except ConnectionError:
    print "Connection error exception thrown"
except ConnectTimeout:
    print "Connect timeout exception thrown"
else:
    print imageList
    print "Names:"
    for image in imageList:
        nameStr = image.tags[0]
        print nameStr
