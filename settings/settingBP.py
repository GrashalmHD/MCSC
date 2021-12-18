import sys
import json
from logging import Formatter
import flask as fl
from flask import render_template,redirect,request,Blueprint
from flask.helpers import url_for
from flask_login import login_required

from settings.settingsFile import loadSettings, saveSettings, settingsDict
from settings.settingsInfos import loadSettingInfos, settingsInfoDict


settingsBP = Blueprint("settings",__name__)


loadSettings()
loadSettingInfos()

@settingsBP.route("/settings")
@login_required
def settings():
    global settingsDict
    global settingsInfoDict

    return render_template("settings.html", settings = settingsInfoDict)

@settingsBP.route("/settings/save",methods=["POST"])
@login_required
def settingsSave():

    global settingsDict
    global settingsInfoDict

    for key, value in settingsDict.items():
        
        try:
            settInfo = settingsInfoDict[key]
        except:
            continue

        newVal = request.form.get(key)

        if settInfo.infos.isBool:
            if newVal == "on":
                newVal = "true"
            else:
                newVal = "false"
        
        elif newVal == None:
            continue

        #print(key + "\t\t | " + newVal)
        settingsDict[key] = str(newVal)
    
    loadSettingInfos()

    ret = {}
    try:
        saveSettings()
        ret["status"] = 1
    except:
        ret["status"] = 0
        print(sys.exc_info()[0])
        

    return redirect(url_for("settings.settings"))