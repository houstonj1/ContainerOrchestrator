from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
import docker
import requests
import humanize

client = docker.from_env()

@app.route('/index')
@app.route('/')
def dashboard():
    # open dashboard page
    containers = client.containers.list(True)
    return render_template('containers.html', script="container.js", css="container.css", containers=containers)
    #<--- for now ---->
    #return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html', script="login.js", css="login.css")

def list_images():
    images = [image.attrs for image in client.images.list()]
    imageList = []
    for image in images:
        [name,tag] = image["RepoTags"][0].split(':')
        size = str(humanize.naturalsize(image["Size"]))
        imageList.append((name,tag,size))
    return imageList

@app.route('/images',methods = ['POST','GET'])
def images():
    imageList = list_images()
    if request.method == 'GET':
        return render_template("images.html", title="Images", script="image.js", css="image.css", imageList=imageList)
    if request.method == 'POST':
        fullPath = request.form['img_path']
        if fullPath == "":
            return redirect(url_for('images_failure'))
        [name,tag] = fullPath.split(':')
        try:
            retVal = client.images.pull(str(name), tag=str(tag))
            return redirect(url_for('images_success'))
        except:
            return redirect(url_for('images_failure'))

@app.route('/images')
def images_failure():
    return images_success()

@app.route('/images')
def images_success():
    imageList = list_images()
    return render_template("images.html", title="Images", script="image.js", css="image.css", imageList=imageList)

@app.route('/containers', methods = ['POST','GET'])
def containers():
    containers = client.containers.list(True)
    if request.method == 'GET':
        return render_template('containers.html', title="Containers", script="container.js", css="Container.css", containers=containers)
    if request.method == 'POST':

        try:
            print containerList
            """for container in containerList:
                container = client.containers.get(container)
                container.stop()
            """
            return render_template('containers.html', title="Containers", script="container.js", css="Container.css", containers=containers)
        except:
            return render_template('containers.html', title="Containers", script="container.js", css="Container.css", containers=containers)


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
