import sys
import docker

client = docker.from_env()

try:
    client.images.list()
except ConnectionError as e:
    print e
