from os import stat
import re
import flask as fl
from flask import render_template,redirect,request,Blueprint
from flask.helpers import send_file
from flask_login import login_required
import json

from serverInfo import serverPath
from console.logHandler import getLogHandler
from status.statusHandler import getServerHandler

logHandler = getLogHandler()
consoleBP = Blueprint("console",__name__)
serverHandler = getServerHandler()

@consoleBP.route("/getlogtxt",methods=["GET"])
@login_required
def getlogtxt():
    return send_file(f"{serverPath}/logs/latest.log",as_attachment=True)



@consoleBP.route("/getlogall",methods=["GET"])
@login_required
def getlogall():
    return render_template('log.html',log=logHandler.getAll())

@consoleBP.route("/console",methods=["GET"])
@login_required
def console():
    return render_template('console.html')

global log
log =[]

@consoleBP.route("/getlog",methods=["GET"])
@login_required
def getlog():
    global logHandler
    
    ret = ""
    for line in logHandler.getLines(50):
        ret = ret + line + "\n"

    resp = fl.Response(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@consoleBP.route("/sendcmd",methods=["POST"])
@login_required
def sendcmd():
    global log
    cmd = request.data.decode('utf-8')
    cmd_json = json.loads(cmd)
    serverHandler.sendCommand(cmd_json['cmd'])
    return ""