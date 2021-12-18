from datetime import time
import sys
import json
from logging import Formatter
import flask as fl
from flask import render_template,redirect,request,Blueprint
from flask.helpers import url_for
from flask_login import login_required
import requests
import time
import uuid

from lists.listFileHandler import loadLists,listData,saveLists

loadLists()

listsBP = Blueprint("lists",__name__)

@listsBP.route("/list/<name>")
@login_required
def lists(name):
    global listData
    try:
        data = listData[name]
    except:
        print(sys.exc_info()[0])
        return redirect(url_for("main.index"))

    return render_template("list.html",list=data,name=name)


@listsBP.route("/list/<name>/delete/<uuid>",methods=["POST"])
@login_required
def delete(name,uuid):
    global listData

    for elem in listData[name]:
        if elem['uuid'] == uuid:
            listData[name].remove(elem)
            break

    try:
        saveLists()
    except:
        pass

    return redirect(url_for("lists.lists",name=name))


@listsBP.route("/list/<name>/add/<pName>",methods=["POST"])
@login_required
def add(name,pName):
    global listData

    res = {}

    unixTime = int(time.time())

    url = f"https://api.mojang.com/users/profiles/minecraft/{pName}?at={unixTime}"

    print(url)

    try:
        r = requests.get(url)

        data = None

        data = r.json()
        
        player = {}

        player['name'] = data['name']
        player['uuid'] = str(uuid.UUID(data['id']))

        listData[name].append(player)

        saveLists()

        res['status'] = 1
    except:
        res['status'] = 0

    return json.dumps(res)