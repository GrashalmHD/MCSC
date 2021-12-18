from auth import login
import flask as fl
from flask.templating import render_template
from flask_login import login_required
import time

main = fl.Blueprint('main',__name__)


class MainVisualComponent:
    name : str
    location : str
    iconData : str
    color : str

    def __init__(self,name,location,iconData,color) -> None:
        self.name = name
        self.location = location
        self.iconData = iconData
        self.color = color

components = []

components.append(MainVisualComponent("Status","status","fa-power-off","green"))
components.append(MainVisualComponent("Settings","settings","fa-cogs","blue"))
components.append(MainVisualComponent("Console","console","fa-terminal","blue"))
components.append(MainVisualComponent("Whitelist","list/Whitelist","far fa-check-circle","green"))
components.append(MainVisualComponent("Banlist","list/Banlist","fas fa-gavel","red"))
components.append(MainVisualComponent("OP List","list/OP-List","fas fa-crown","gold"))
components.append(MainVisualComponent("World","world","fa-cube","#567d46"))


@main.route("/",methods=['GET'])
@login_required
def index():

    cols = 2
    rows = len(components) / cols

    return render_template("main.html",components = components, rows = rows, cols = cols)

@main.route("/about",methods=['GET'])
@login_required
def about():
    return render_template("about.html")
        