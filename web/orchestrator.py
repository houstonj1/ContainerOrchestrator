from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
import docker
import requests
import json

client = docker.from_env()

@app.route('/')
def dashboard():
    # open dashboard page
    return 'Dashboard'

@app.route('/login',)
def login():
    return 'Login page'

def list_images():
    images = [image.attrs for image in client.images.list()]
    imageList = [str(image["RepoTags"][0]) for image in images]
    images = '<ul>\n'
    if imageList:
        for image in imageList:
            images += '<li>' + image + '</li>\n'
    return '<h1>Images page</h1>\n' + images

@app.route('/images',methods = ['POST','GET'])
def images():
    print request.method
    if request.method == 'GET':
        return list_images()
    if request.method == 'POST':
        name = request.form['image']
        tag = request.form['tag']
        print name
        print tag
        retVal = client.images.pull(name, tag=tag)
        print retVal
        return list_images()

@app.route('/containers')
def containers():
    containers = client.containers.list(True)
    return render_template('Container.html', containers=containers)


@app.route('/containers/<id>')
def container_info(id):
    # check to see if there is a container with this id
    idList = [container.name for container in client.containers.list(True)]
    print idList
    if id in idList:
        return 'Container %s requested' % id
    else:
        return redirect(url_for('containers'))

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, True)
