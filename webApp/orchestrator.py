from __future__ import print_function
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
from flask_login import LoginManager
import docker
import time
import json
import requests
import sys
import humanize
app = Flask(__name__)
app.secret_key = "ThisIScontainerOrchestrator\x1c02\xbbh\xba\xd8$\xe9d(\xa5\xe0Wb\xff\x1a\x8a\xd391\x1a(N\x8c"
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'container'
app.config['MYSQL_DATABASE_DB'] = 'ContainerOrchestrator'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
client = docker.from_env()
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")

    return render_template('home.html', scripts=["home.js","fusioncharts.js","fusioncharts.charts.js","themes/fusioncharts.theme.zune.js","createChart.js"], css="home.css", version="",cpu="",memory="",hdd="")

@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = connection.cursor()
    cursor.execute("SELECT * from account where username=\'" + username + "\' and password=\'" + password + "\'")
    data = cursor.fetchone()
    if data is None:
        flash('Invalid login!')
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        session['username'] = username
        cursor = connection.cursor()
        cursor.execute("SELECT userID from account where username=\'" + username + "\'")
        data = cursor.fetchone()[0]
        print(data, file=sys.stderr)
        session['user_id'] = data
        session['logged_in'] = True
        return home()

@app.route('/login/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirm-password']
    if password != confirmPassword:
        flash('Passwords do not match!')
        return render_template('login.html', scripts=["login.js"], css="login.css")
    cursor = connection.cursor()
    cursor.execute("SELECT userID from account where username=\'" + username + "\'")
    data = cursor.fetchone()
    if data is not None:
        flash('Invalid username! The specifed username is already taken, please choose a different username.')
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        query = "INSERT INTO account (username,password) values(\'"+ str(username) + "\',\'" + str(password) + "\');"
        cursor.execute(query)
        connection.commit()
        flash('Successfully registered! Please log in.')
        return render_template('login.html', scripts=["login.js"], css="login.css")

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

# IMAGES #

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
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        imageList = list_images()
        if request.method == 'GET':
            return render_template("images.html", title="Images", scripts=["image.js"], css="image.css", imageList=imageList)
        if request.method == 'POST':
            fullPath = request.form['img_path']
            # need html form validation
            [name,tag] = fullPath.split(':')
            try:
                retVal = client.images.pull(str(name), tag=str(tag))
                return images()
            except:
                return images()

# CONTAINERS #

def list_containers():

    return containers

def get_container(id):
    container = client.containers.get(id)
    return container

@app.route('/containers', methods = ['POST','GET'])
def containers():
    cursor = connection.cursor()
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        if request.method == 'GET':
            containers = client.containers.list(True)
            newContainers = []
            for container in containers:
                print("HERE", file=sys.stderr)
                query = "SELECT username from account where userID=(select createBy from container where containerID=\'" + str(container.name) + "\');"
                cursor.execute(query)
                data = cursor.fetchone()
                if data is None:
                    data = "SysAdmin"
                else:
                    data = data[0]
                newContainers.append((container,str(data)))
            print(newContainers,file=sys.stderr)
            return render_template('containers.html', title="Containers", scripts=["container.js"], css="container.css", containers=newContainers)
        if request.method == 'POST':
            userAction = request.form['data']
            userAction = userAction.split(',')
            action = userAction[0]
            ids = userAction[1:]
            for id in ids:
                container = get_container(id)
                if action == "Start":
                    container.start()
                elif action == "Stop":
                    container.stop()
                elif action == "Remove":
                    container.remove()
            newContainers = []
            containers = client.containers.list(True)
            for container in containers:
                query = "SELECT username from account where userID=(select createBy from container where containerID=\'" + str(container.name) + "\');"
                cursor.execute(query)
                data = cursor.fetchone()
                data = cursor.fetchone()
                if data is None:
                    data = "SysAdmin"
                else:
                    data = data[0]
                newContainers.append((container,str(data)))
            print(newContainers,file=sys.stderr)
            return render_template('container_table.html', containers=newContainers)

@app.route('/containers/create', methods=['POST'])
def containers_create():
    if request.method == 'POST':
        containerData = request.form['data']
        containerData = containerData.split(',')
        name = containerData[0]
        image = containerData[1]
        command = containerData[2]
        detach = True if containerData[3] == "True" else False
        hostname = containerData[4]
        netDisabled = True if containerData[5] == "True" else False
        if containerData[6] in ["bridge", "host", "none"]:
            netMode = containerData[6]
        else:
            netMode = "none"
        mac = containerData[7]
        # TODO -- need to test this
        ports = containerData[8]
        pubPorts = True if containerData[5] == "True" else False
        try:
            client.containers.create(image,command,detach=detach,hostname=hostname,name=name,network_disabled=netDisabled,network_mode=netMode,mac_address=mac,ports=ports,publish_all_ports=pubPorts)
            userID = session['user_id']
            cursor = connection.cursor()
            query = "INSERT INTO container (containerID,imageName,createBy) values(\'"+ str(name) + "\',\'" + str(image) + "\',\'" + str(userID) + "\');"
            cursor.execute(query)
            connection.commit()
            newContainers=[]
            containers = client.containers.list(True)
            for container in containers:
                query = "SELECT username from account where userID=(select createBy from container where containerID=\'" + str(container.name) + "\');"
                cursor.execute(query)
                data = cursor.fetchone()
                if data is None:
                    data = "SysAdmin"
                else:
                    data = data[0]
                newContainers.append(container,str(data))
            print(newContainers,file=sys.stderr)
            return render_template('container_table.html', containers=newContainers)
        except:
            # TODO need docker exception here
            return sys.exc_info()[0]

@app.route('/containers/<id>')
def container_info(id):
    idList = [container.name for container in client.containers.list(True)]
    if id in idList:
        container = client.containers.get(id)
        return render_template('containerInfo.html', title="Container Info", scripts=["containerinfo.js"], css="containerinfo.css", container=container)
    else:
        return redirect(url_for('containers'))

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, True)
