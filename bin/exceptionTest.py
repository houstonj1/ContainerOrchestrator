#!/usr/bin/python

import docker
import requests
from docker import *
from requests import ConnectionError

client = docker.from_env()

try:
    client.images.list()
except ConnectionError,e:
    print 'worked'
else:
    print ':('

#   fh = open("testfile", "w")
#   fh.write("This is my test file for exception handling!!")
#except IOError:
#   print "Error: can\'t find file or read data"
#else:
#   print "Written content in the file successfully"
#   fh.close()
                                                              23,1          Top
