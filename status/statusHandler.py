from _thread import start_new_thread as snt
import os
import subprocess
import time
from subprocess import STDOUT, Popen, PIPE
import psutil

from serverInfo import serverPath
from sse.eventStack import getEventStackHandler
eventStackHandler = getEventStackHandler()

statusHandler = None


def getStatusHandler():
    global statusHandler

    if statusHandler == None:
        statusHandler = StatusHandler()

    return statusHandler

serverHandler = None

def getServerHandler():
    global serverHandler

    if serverHandler == None:
        serverHandler = ServerHandler()

    return serverHandler

class ServerHandler:

    process = None

    def __init__(self) -> None:
        pass

    def isRunning(self) -> bool:
        if not self.process == None:

            poll = self.process.poll()

            if poll == None:
                return True
        
        return False

    def start(self):
        if not self.isRunning():
            print("start")
            if not os.path.exists(f"{serverPath}/mcserverfifo"):
                os.popen(f"mkfifo {serverPath}/mcserverfifo")

            self.process = Popen(["bash", f"{serverPath}/server.sh"],cwd=serverPath)
            eventStackHandler.addEvent("Starting server...")
        else:
            eventStackHandler.addEvent("Server already running")


    def stop(self):
        if self.isRunning():
            self.sendCommand('/stop')
            eventStackHandler.addEvent("Stopping server...")

    def sendCommand(self,command):
        if self.isRunning():
            print(f"Sending command '{command}'")
            with open(f"{serverPath}/mcserverfifo","w") as f:
                command = command + '\n'
                f.write(command)

class StatusHandler:

    cpu:int = 0
    ram:int = 0
    status:bool = False

    serverHandle = None

    running:bool = False

    def __init__(self) -> None:
        self.serverHandle = getServerHandler()
        pass

    def startServer(self):
        self.serverHandle.start()

    def stopServer(self):
        self.serverHandle.stop()

    def run(self):
        if not self.running:
            self.running = True
            snt(self.readData,())
            snt(self.getStatus,())
        else:
            pass

    def stop(self):
        self.running = False

    def restartServer(self):
        eventStackHandler.addEvent("Restarting Server")
        self.stopServer()

        while self.running:
            pass

        self.startServer()

    def readData(self):
        while self.running:
            
            time.sleep(1)
            
            self.cpu = psutil.cpu_percent()
            self.ram = psutil.virtual_memory().percent

    def getStatus(self):
        while self.running:

            time.sleep(1)

            self.status = self.serverHandle.isRunning()

