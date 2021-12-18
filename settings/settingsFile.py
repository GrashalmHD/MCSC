from serverInfo import serverPath

settingsDict = {}

def loadSettings():

    global settingsDict

    lines = []
    with open(f"{serverPath}/server.properties","r") as f:
        lines = f.readlines()
    
    for line in lines:

        line.replace("\n","")

        if line.startswith('#'):
            continue
        if not line.__contains__("="):
            continue

        lineParts = line.split("=")

        settingsDict[lineParts[0]] = lineParts[1].replace("\n","")

    print("Settings loaded!")


def saveSettings():

    global settingsDict

    content = ""
    with open(f"{serverPath}/server.properties", "w") as f:
        
        for key, value in settingsDict.items():
            content += key + "=" + value +"\n"

        f.write(content)

