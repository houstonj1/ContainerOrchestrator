from __future__ import print_function
from datetime import timedelta
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
import docker
from docker.errors import APIError
import time
import json
import psutil
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

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

def log(msgs):
    """
    Logging function for Flask. Uses import __future__ to get python3 print()
    """
    for message in msgs:
        print("FLASK::LOG::" + str(message), file=sys.stderr)

def call_db(query,commitFlag):
    cursor = connection.cursor()
    cursor.execute(query)
    log(["DB executing query: " + query])
    log([str(commitFlag)])
    if commitFlag:
        connection.commit()
        return None
    else:
        retVal = cursor.fetchall()
        log([str(retVal)])
        if str(retVal) == '()':
            return None
        return retVal

@app.route('/login', methods = ['POST'])
def login():
    """
    Login page. This will validate provided login credentials and return the home page. If invalid, it will flash an error.
    """
    username = request.form['username']
    password = request.form['password']
    retVal = call_db("SELECT * from account where username=\'" + username + "\' and password=\'" + password + "\'", False)
    if retVal is None:
        error = 'Invalid login!'
        return render_template('login.html', scripts=["login.js"], css="login.css", error=error)
    else:
        session['username'] = username
        retVal = call_db("SELECT userID from account where username=\'" + session['username'] + "\'", False)
        session['user_id'] = retVal[0][0]
        session['logged_in'] = True
        return redirect(url_for('home'))

@app.route('/login/register', methods=['POST'])
def register():
    """
    Register page. This will allow a user to register for an account.
    """
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirm-password']
    if password != confirmPassword:
        error = 'Passwords do not match!'
        return render_template('login.html', scripts=["login.js"], css="login.css", errorReg=error)
    retVal = call_db("SELECT userID from account where username=\'" + username + "\'", False)
    log(["Register db return: " + str(retVal)])
    if retVal is not None:
        error = 'Invalid username! The specifed username is already taken, please choose a different username.'
        return render_template('login.html', scripts=["login.js"], css="login.css", errorReg=error)
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

@app.route('/logout')
def logout():
    """
    Logout page. This will log the user out, then return the login page.
    """
    session['logged_in'] = False
    return home()

# IMAGES #

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
        errorList = set()
        imageList = list_images()
        if request.method == 'GET':
            return render_template("images.html", title="Images", scripts=["image.js"], css="image.css", imageList=imageList)
        if request.method == 'POST':
            fullPath = request.form['name']
            log([fullPath])
            try:
                log(["begin pull", fullPath])
                retVal = client.images.pull(str(fullPath))
                log(["end pull"])
            except APIError as e:
                e = str(e)
                if "Timeout" in e:
                    errorList.add("Request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers) Make sure image is valid.")

            imageList = list_images()
            return render_template("image_table.html", imageList=imageList, pullErrors=errorList)

@app.route('/images/pull_name_fail', methods=['POST'])
def pull_name_fail():
    if request.method == 'POST':
        log(["HERE RE POST"])
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
    log([request.method == 'POST'])
    errorList = set()
    if request.method != 'POST':
        return images()
    else:
        imageList = request.form['list'].split(',')
        log([imageList])
        for image in imageList:
            try:
                client.images.remove(image)
            except APIError as e:
                e = str(e)
                e = e[e.find('(')+1:e.rfind(')')]
                e = e[1:-1]
                log([e])
                errorList.add(e.replace('(must force)',''))

        imageList = list_images()
        return render_template("image_table.html", imageList=imageList, removeErrors=errorList)



# CONTAINERS #

def list_containers():
    """
    List containers function. This will return a list of all containers on the system as well as their owner.
    If the container was created outside of the web application, the owner will be SysAdmin
    """
    myList = []
    for container in client.containers.list(True):
        retVal = call_db("SELECT username from account where userID=(select createBy from container where containerID=\'" + str(container.name) + "\');", False)
        user = "SysAdmin" if retVal is None else str(retVal[0][0])
        log(["List user:" + user])
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
            userAction = request.form['data'].split(',')
            action = userAction[0]
            ids = userAction[1:]
            log(["Container IDs requesting an action:",str(ids),"Action:",str(action)])
            containerList = [get_container(id) for id in ids]
            if action == "Start" or action == "Stop":
                for container in containerList:
                    if action == "Start":
                        container.start()
                    elif action == "Stop":
                        container.stop()
            elif action == "Remove":
                retVal = call_db("SELECT containerID from container where createBy=\'" + str(session['user_id']) + "\';", False)
                retVal = set(name[0] for name in retVal)
                log(["List of containers owned by user:", str(retVal)])
                nameSet = set(container.name for container in containerList)
                log(["List of containers checked:", str(nameSet)])
                for name in nameSet:
                    if not nameSet.issubset(retVal):
                        return "fail"
                for name in nameSet:
                    container = get_container(name)
                    container.remove()
                    retVal = call_db("DELETE from container where containerID=\'" + name + "\';", True)

            containerList = list_containers()
            return render_template('container_table.html', containers=containerList)

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
            cursor = connection.cursor()
            query = "INSERT INTO container (containerID,imageName,createBy) values(\'"+ str(name) + "\',\'" + str(image) + "\',\'" + str(session['user_id']) + "\');"
            cursor.execute(query)
            connection.commit()
            log(["Container created, returning", str(url_for('containers'))])
            containerList = list_containers()
            log(["Container list", str(containerList)])
            return render_template('container_table.html', containers=containerList)
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

@app.route('/chart', methods=['POST'])
def get_chart_info():
    dataList = []
    cursor = connection.cursor()
    query = "SELECT imageName, count(*) as NUM FROM container GROUP BY imageName;"
    cursor.execute(query)
    retVal = cursor.fetchall()
    for tup in retVal:
        dataList.append({"label":str(tup[0]), "value":str(tup[1])})

    return jsonify(dataList)

if __name__ == '__main__':
    app.run('0.0.0.0', 5001, True)
