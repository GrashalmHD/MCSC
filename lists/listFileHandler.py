import json
from serverInfo import serverPath

lists = [
    {
        "name":"Whitelist",
        "loc":f"{serverPath}/whitelist.json"
    },
    {
        "name":"Banlist",
        "loc":f"{serverPath}/banned-players.json"
    },
    {
        "name":"OP-List",
        "loc":f"{serverPath}/ops.json"
    }
]

listData = {}

def loadLists():

    global listData

    for list in lists:
        with open(list["loc"],"r") as f:
            data = f.read()
            data_json = json.loads(data)
            listData[list["name"]] = data_json
            print(list["name"] + " loaded!")
            
def saveLists():
    for list in lists:
        with open(list['loc'],'w') as f:
            name = list['name']
            data = json.dumps(listData[name])
            f.write(data)