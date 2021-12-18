import zipfile
import shutil
import traceback
import os
import sys
import json
from logging import Formatter, currentframe, log
import flask as fl
from flask import render_template,redirect,request,Blueprint,send_from_directory
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import environ_property

from world.worldHandler import addWorld, loadWorldData,changeWorldName,setWorldActive,checkID,getPath,getName,deleteWorld
from settings.settingsFile import settingsDict,saveSettings
from status.statusHandler import getStatusHandler
from serverInfo import serverPath

from sse.eventStack import getEventStackHandler
eventStackHandler = getEventStackHandler()

worldData = loadWorldData()

worldBP = Blueprint("world",__name__)

statusHandler = getStatusHandler()


@worldBP.route("/world")
@login_required
def world():
    
    global worldData
    global settingsDict

    if not settingsDict['level-name'] == worldData['active']:
        worldData = setWorldActive(settingsDict['level-name'])

    return render_template("world.html",worlds = worldData['list'], active = worldData['active'])

@worldBP.route("/world/<id>/getIcon")
@login_required
def getIconID(id):

    global worldData

    path = ""

    try:
        path = getPath(id)
    except:
        print(sys.exc_info()[0])
        return "",404

    print("<->")
    print(path)
    return send_from_directory(path,"icon.png")

@worldBP.route('/world/<id>/changeName',methods=["POST"])
@login_required
def changeName(id):

    data = json.loads(request.get_data())    
    try:
        worldData = changeWorldName(data['name'],id)
    except:
        traceback.print_exc()
        eventStackHandler.addEvent("Failed to change name")
        return "",500
    eventStackHandler.addEvent("Changed name")
    return "",200

@worldBP.route("/world/<id>/setActive",methods=["POST"])
@login_required
def setActive(id):

    global worldData
    global settingsDict
    global statusHandler

    if not checkID(id):
        return "",500
    
    settingsDict['level-name'] = id
    saveSettings()

    worldData = setWorldActive(id)

    eventStackHandler.addEvent("Set new active world")

    #Restart Server
    statusHandler.restartServer()

    return "",200

@worldBP.route("/world/<id>/download")
@login_required
def download(id):

    if not checkID(id):
        return "",500

    if os.path.exists("world/temp.zip"):
        os.remove("world/temp.zip")

    path = getPath(id,False)

    print(path)

    cmd = f"cd {serverPath} && zip -r world/temp.zip {path}"

    os.system(cmd)
    eventStackHandler.addEvent("Sending download...")
    return send_from_directory("world","temp.zip",as_attachment=True,attachment_filename=getName(id)+".zip")


@worldBP.route('/world/<id>/delete',methods=["POST"])
@login_required
def delete(id):

    if not checkID(id):
        return "",500

    if worldData['active'] == id:
        eventStackHandler.addEvent("Can not delete active world")
        return "",500

    deleteWorld(id)

    shutil.rmtree(f"{serverPath}/{id}")
    eventStackHandler.addEvent("Deletion successful")
    return "",200


@worldBP.route("/world/upload",methods=["POST"])
@login_required
def upload():

    global worldData

    #Save .zip File

    eventStackHandler.addEvent("Saving file...")

    worldZip = request.files['world']

    worldZip.save("world/upload/upload.zip")

    #Unzip file

    eventStackHandler.addEvent("Decompressing world...")

    os.system("cd world/upload && unzip upload.zip")

    os.remove("world/upload/upload.zip")

    id,data = addWorld(worldZip.filename)

    subFolders = [f.name for f in os.scandir("world/upload/") if f.is_dir()]

    oldName = subFolders[0]

    #Move and rename world

    eventStackHandler.addEvent("Installing world...")

    shutil.move(f"world/upload/{oldName}",f"{serverPath}/{id}")

    worldData = data

    eventStackHandler.addEvent("World uploaded")

    return "",200