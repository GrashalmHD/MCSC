import uuid
import json
import sys

from flask.typing import BeforeRequestCallable
from serverInfo import serverPath

worldData = []

def writeDataToFile():
    global worldData

    with open('world/worlds.json','w') as f:
            f.write(json.dumps(worldData))


def loadWorldData():

    global worldData
    #global activeWorld

    data = None
  
    with open("world/worlds.json","r") as f:
        data = json.loads(f.read())
    
    print("World data loaded!")
    worldData = data
    return data

def changeWorldName(name,id):
    global worldData
    i = 0
    for world in worldData['list']:
        if world['id'] == id:
            worldData['list'][i]['name'] = name
            break

        i+=1
    
    writeDataToFile()

    print(worldData , i)
    return worldData

def setWorldActive(id):

    global worldData

    worldData['active'] = id

    writeDataToFile()

    return worldData

def checkID(id):
    global worldData

    if getWorld(id) != None:
        return True

    return False

def getPath(id, world_folder = True):
    global worldData

    if world_folder:
        path = f"{serverPath}/"
    else:
        path = ""

    path += id

    return path

def getName(id):
    
    return getWorld(id)['name']

def getWorld(id):
    
    for world in worldData['list']:
        if world['id'] == id:
            return world

    return None
    

def deleteWorld(id):
    global worldData

    worldData['list'].remove(getWorld(id))

    writeDataToFile()

    return worldData

def addWorld(name):
    global worldData

    world = {}

    id = str(uuid.uuid4())
    world['id'] = id
    world['name'] = name

    worldData['list'].append(world)

    writeDataToFile()

    return id,worldData