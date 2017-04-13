from __future__ import print_function
from datetime import timedelta
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
import docker
import requests
from docker.errors import APIError
from docker.errors import ImageNotFound
from requests import ConnectTimeout
from requests import ConnectionError
import ast
import time
import psutil
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

def log(msgs):
    """
    Logging function for Flask. Uses import __future__ to get python3 print()
    """
    for message in msgs:
        print("FLASK::LOG::" + str(message), file=sys.stderr)

def call_db(query,commitFlag):
    cursor = connection.cursor()
    cursor.execute(query)
    if commitFlag:
        connection.commit()
        return None
    else:
        retVal = cursor.fetchall()
        if str(retVal) == '()':
            return None
        return retVal

## Website architechure pages ##

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)

@app.route('/login', methods = ['POST'])
def login():
    """
    Login page. This will validate provided login credentials and return the home page. If invalid, it will flash an error.
    """
    username = request.form['username']
    password = request.form['password']
    retVal = call_db("SELECT * from account where username=\'" + username + "\' and password=\'" + password + "\'", False)
    if retVal is None:
        error = 'ERROR: Invalid login. Please try again.'
        return render_template('login.html', scripts=["login.js"], css="login.css", error=error)
    else:
        session['username'] = username
        retVal = call_db("SELECT userID from account where username=\'" + session['username'] + "\'", False)
        session['user_id'] = retVal[0][0]
        session['logged_in'] = True
        return redirect(url_for('home'))

@app.route('/login/forgot_password', methods=['POST'])
def forgot_password():
    error = "Please contact your System Administrator to reset your password."
    return render_template('login.html', scripts=["login.js"], css="login.css", error=error)

@app.route('/login/register', methods=['POST'])
def register():
    """
    Register page. This will allow a user to register for an account.
    """
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirm-password']
    if password != confirmPassword:
        error = 'ERROR: Passwords do not match! Please try again.'
        return render_template('login.html', scripts=["login.js"], css="login.css", error=error)
    retVal = call_db("SELECT userID from account where username=\'" + username + "\'", False)
    if retVal is not None:
        error = 'ERROR: Invalid username! The specifed username is already taken, please choose a different username.'
        return render_template('login.html', scripts=["login.js"], css="login.css", error=error)
    else:
        retVal = call_db("INSERT INTO account (username,password) values(\'"+ str(username) + "\',\'" + str(password) + "\');", True)
        success = 'Successfully registered! Please log in.'
        return render_template('login.html', scripts=["login.js"], css="login.css", success=success)

@app.route('/')
def home():
    """
    Home page. This will return the login page if the user is not logged in.
    """
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")

    # Get system information
    dockerVersion = str(client.version()['Version'])
    numCPUs = psutil.cpu_count()
    psObj = psutil.virtual_memory()
    memUsed = humanize.naturalsize(psObj.used).split(' ')[0]
    memTotal = humanize.naturalsize(psObj.total)
    psObj = psutil.disk_usage('/')
    diskUsed = humanize.naturalsize(psObj.used).split(' ')[0]
    diskTotal = humanize.naturalsize(psObj.total)
    return render_template('home.html',scripts=["home.js","fusioncharts.js","fusioncharts.charts.js","themes/fusioncharts.theme.zune.js","createChart.js"],css="home.css",version=dockerVersion,cpus=numCPUs,memU=memUsed,memT=memTotal,diskU=diskUsed,diskT=diskTotal)

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html', scripts=["help.js"], title="Help Page", css="help.css")

@app.route('/chart', methods=['GET'])
def get_chart_info():
    dataList = []
    cursor = connection.cursor()
    query = "SELECT imageName, count(*) as NUM FROM container GROUP BY imageName;"
    cursor.execute(query)
    retVal = cursor.fetchall()
    for tup in retVal:
        dataList.append({"label":str(tup[0]), "value":str(tup[1])})

    return jsonify(dataList)

@app.route('/logout')
def logout():
    """
    Logout page. This will log the user out, then return the login page.
    """
    session['logged_in'] = False
    return home()

## Images ##

def list_images():
    """
    List images function. This will return a list of all images on the system.
    """
    images = [image.attrs for image in client.images.list()]
    imageList = []
    for image in images:
        [name,tag] = image["RepoTags"][0].split(':')
        size = str(humanize.naturalsize(image["Size"]))
        imageList.append((name,tag,size))
    return imageList

@app.route('/images',methods = ['POST','GET'])
def images():
    """
    Images page. This will return the images page. Also includes POST logic for pulling an image.
    """
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        if request.method == 'GET':
            imageList = list_images()
            return render_template("images.html", title="Images", scripts=["image.js"], css="image.css", imageList=imageList)
        if request.method == 'POST':
            errorList = set()
            fullPath = request.form['name']
            try:
                retVal = client.images.pull(str(fullPath))
            except APIError as e:
                e = str(e)
                if "Timeout" in e:
                    errorList.add("Request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers) Make sure image is valid.")
                else:
                    errorList.add(e)
            except ImageNotFound as e:
                e = str(e)
                log([e])
                errorList.add(e)
            except ConnectTimeout as e:
                e = str(e)
                log([e])
                errorList.add(e)
            except ConnectionError as e:
                e = str(e)
                log([e])
                errorList.add(e)

            imageList = list_images()
            return render_template("image_table.html", imageList=imageList, pullErrors=errorList)

@app.route('/images/pull_name_fail', methods=['POST'])
def pull_name_fail():
    if request.method == 'POST':
        errorList = set()
        errorList.add("Invalid image name. Required format 'image:tag'")
        imageList = list_images()
        return render_template("image_table.html", imageList=imageList, pullErrors=errorList)

@app.route('/images/remove', methods = ['POST'])
def remove_image():
    """
    Remove image page. This page is sent a POST request when a user wants to remove selected images.
    It will return the updated images table
    """
    errorList = set()
    if request.method != 'POST':
        imageList = list_images()
        return render_template("image_table.html", imageList=imageList)
    else:
        imageList = request.form['list'].split(',')
        for image in imageList:
            try:
                client.images.remove(image)
            except APIError as e:
                e = str(e)
                e = e[e.find('(')+1:e.rfind(')')]
                e = e[1:-1]
                log([e])
                errorList.add(e.replace('(must force)',''))
            except ConnectTimeout as e:
                e = str(e)
                log([e])
                errorList.add(e)
            except ConnectionError as e:
                e = str(e)
                log([e])
                errorList.add(e)

        imageList = list_images()
        return render_template("image_table.html", imageList=imageList, removeErrors=errorList)

## Containers ##

def list_containers():
    """
    List containers function. This will return a list of all containers on the system as well as their owner.
    If the container was created outside of the web application, the owner will be SysAdmin
    """
    myList = []
    for container in client.containers.list(True):
        retVal = call_db("SELECT username from account where userID=(select createBy from container where containerID=\'" + str(container.name) + "\');", False)
        user = "SysAdmin" if retVal is None else str(retVal[0][0])
        myList.append((container,user))
    return myList

def get_container(id):
    """
    Get container function. This will return a container object for the given container ID.
    """
    containerObject = client.containers.get(id)
    return containerObject

@app.route('/containers', methods = ['POST','GET'])
def containers():
    """
    Containers page. This will return the containers page with the list of containers on the system.
    It also contains the POST logic for stopping, starting and removing containers.
    """
    if not session.get('logged_in'):
        return render_template('login.html', scripts=["login.js"], css="login.css")
    else:
        if request.method == 'GET':
            containerList = list_containers()
            return render_template('containers.html', title="Containers", scripts=["container.js"], css="container.css", containers=containerList)
        if request.method == 'POST':
            errorList = set()
            userAction = str(request.form['data'])
            userAction = userAction.split(',')
            action = userAction[0]
            ids = userAction[1:]
            if len(ids) == 1 and ids[0] == '':
                errorList.add("No containers selected!")
                containerList = list_containers()
                return render_template('container_table.html', containers=containerList, errors=errorList)
            containerList = [get_container(id) for id in ids]
            if action == "Start" or action == "Stop":
                for container in containerList:
                    if action == "Start":
                        try:
                            container.start()
                        except APIError as e:
                            e = str(e)
                            e = e[e.find('(')+1:e.rfind(')')]
                            e = e[1:-1]
                            log([e])
                            errorList.add(e)
                        except ConnectTimeout as e:
                            e = str(e)
                            log([e])
                            errorList.add(e)
                        except ConnectionError as e:
                            e = str(e)
                            log([e])
                            errorList.add(e)
                    elif action == "Stop":
                        try:
                            container.stop()
                        except APIError as e:
                            e = str(e)
                            e = e[e.find('(')+1:e.rfind(')')]
                            e = e[1:-1]
                            log([e])
                            errorList.add(e)
                        except ConnectTimeout as e:
                            e = str(e)
                            log([e])
                            errorList.add(e)
                        except ConnectionError as e:
                            e = str(e)
                            log([e])
                            errorList.add(e)
            elif action == "Remove":
                retVal = call_db("SELECT containerID from container where createBy=\'" + str(session['user_id']) + "\';", False)
                if retVal == None:
                    errorList.add("You cannot remove containers created by another user!")
                    containerList = list_containers()
                    return render_template('container_table.html', containers=containerList, errors=errorList)
                retVal = set(name[0] for name in retVal)
                nameSet = set(container.name for container in containerList)
                for name in nameSet:
                    if not nameSet.issubset(retVal):
                        errorList.add("You cannot remove containers created by another user!")
                if errorList:
                    containerList = list_containers()
                    return render_template('containers_table.html', containers=containerList, errors=errorList)
                for name in nameSet:
                    container = get_container(name)
                    try:
                        container.remove()
                        retVal = call_db("DELETE from container where containerID=\'" + name + "\';", True)
                    except APIError as e:
                        e = str(e)
                        e = e[e.find('(')+1:e.rfind(')')]
                        e = e[1:-10]
                        log([e])
                        errorList.add(e)
                    except ConnectTimeout as e:
                        e = str(e)
                        log([e])
                        errorList.add(e)
                    except ConnectionError as e:
                        e = str(e)
                        log([e])
                        errorList.add(e)

            containerList = list_containers()
            return render_template('container_table.html', containers=containerList, errors=errorList)

@app.route('/containers/create', methods=['POST'])
def containers_create():
    if request.method == 'POST':
        errorList = set()
        containerData = str(request.form['data'])
        log([containerData])
        containerData = containerData.split(',')
        name = containerData[0]
        image = containerData[1]
        command = containerData[2]
        hostname = containerData[3]
        netDisabled = True if containerData[4] == "True" else False
        netMode = containerData[5]
        mac = containerData[6]
        ports = containerData[7]
        if ports != '':
            ports = ports.split(':')
            ports = ast.literal_eval("{'" + ports[0] + "':'" + ports[1] + "'}")
        pubPorts = True if containerData[8] == "True" else False
        try:
            client.containers.create(image,command,hostname=hostname,name=name,network_disabled=netDisabled,network_mode=netMode,mac_address=mac,ports=ports,publish_all_ports=pubPorts)
            retVal = call_db("INSERT INTO container (containerID,imageName,createBy) values(\'"+ str(name) + "\',\'" + str(image) + "\',\'" + str(session['user_id']) + "\');", True)
        except APIError as e:
            e = str(e)
            log([e])
            e = e[e.find('(')+1:e.rfind(')')]
            e = e[1:-1]
            errorList.add(e)
        except ConnectTimeout as e:
            e = str(e)
            log([e])
            errorList.add(e)
        except ConnectionError as e:
            e = str(e)
            log([e])
            errorList.add(e)

        containerList = list_containers()
        return render_template('container_create_table.html', containers=containerList, errors=errorList)

@app.route('/containers/<id>')
def container_info(id):
    idList = [container.name for container in client.containers.list(True)]
    if id in idList:
        container = client.containers.get(id)
        ports = container.attrs["NetworkSettings"]["Ports"]
        if ports != None:
            containerPort = str(ports.keys()[0])
            hostPort = str(ports.values()[0][0]["HostIp"]) +':' + str(ports.values()[0][0]["HostPort"])
            return render_template('containerInfo.html', title="Container Info", scripts=["containerinfo.js"], css="containerinfo.css", container=container, hostPort=hostPort, containerPort=containerPort)
        return render_template('containerInfo.html', title="Container Info", scripts=["containerinfo.js"], css="containerinfo.css", container=container)
    else:
        return redirect(url_for('containers'))

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, True)
