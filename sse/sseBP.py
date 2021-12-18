import flask as fl
from flask_login import login_required
import time

from werkzeug.utils import environ_property

from sse.eventStack import getEventStackHandler

eventStackHandler = getEventStackHandler()

eventStackHandler.start()

#eventStackgenerator = eventStackHandler.getGenerator()

sseBP = fl.Blueprint("sse",__name__)

@sseBP.route("/test")
@login_required
def test():
    global eventStack
    global eventStackHandler
    eventStackHandler.addEvent(str(time.time()))
    return "",200



@sseBP.route("/lastUpdate")
def lastUpdate():
    return eventStackHandler.last_message,200

@sseBP.route("/stream")
def stream():
    return fl.Response(eventStackHandler.run(), mimetype="text/event-stream")