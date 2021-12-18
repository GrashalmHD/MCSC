import json
from os import cpu_count, stat
import flask as fl
from flask import render_template,redirect,request,Blueprint
from flask_login import login_required
from status.statusHandler import getStatusHandler

statusBP = Blueprint("status",__name__)

@statusBP.route("/status")
@login_required
def status():
    return render_template('status.html')



statHandler = getStatusHandler()
statHandler.run()

@statusBP.route("/status/get")
@login_required
def getStatus():

    global statHandler

    data = {}
    
    if statHandler.status == True:
        data["serverStatus"] = "Running"
    else:
        data["serverStatus"] = "Stopped"
        
    
    data["cpuLoad"] = statHandler.cpu
    data["ramLoad"] = statHandler.ram

    return json.dumps(data)

@statusBP.route("/status/server/toggle")
@login_required
def serverToggle():

    global statHandler

    if statHandler.status:
        statHandler.stopServer()
    else:
        statHandler.startServer()

    return ""