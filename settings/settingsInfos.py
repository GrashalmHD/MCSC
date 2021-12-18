from logging import info
from os import truncate
from typing import Set

from flask.helpers import flash

from settings.settingsFile import settingsDict

class Setting:

    key:str
    description:str
    show:bool
    
    isStr:bool
    isInt:bool
    isBool:bool

    def __init__(self,key,description,show,isStr = False,isInt = False, isBool = False) -> None:
        
        self.key = key
        self.description = description
        self.isStr = isStr
        self.isInt = isInt
        self.isBool = isBool
        self.show = show


class SettingVal:

    infos:Setting
    val:str

    def __init__(self,infos,val) -> None:
        
        self.infos = infos
        self.val = val


settings = []
settingsInfoDict = {}


settings.append(Setting("enable-jmx-monitoring","description",False,isBool=True))
settings.append(Setting("rcon.port","description",False,isInt=True))
settings.append(Setting("level-seed","description",True,isInt=True))
settings.append(Setting("gamemode","description",True,isStr=True))
settings.append(Setting("enable-command-block","description",True,isBool=True))
settings.append(Setting("enable-query","description",False,isBool=True))
settings.append(Setting("generator-settings","description",False,isStr=True))
settings.append(Setting("level-name","description",False,isStr=True))
settings.append(Setting("motd","description",False,isStr=True))
settings.append(Setting("query.port","description",False,isInt=True))
settings.append(Setting("pvp","description",True,isBool=True))
settings.append(Setting("generate-structures","description",True,isBool=True))
settings.append(Setting("difficulty","description",True,isStr=True))
settings.append(Setting("network-compression-threshold","description",False,isInt=True))
settings.append(Setting("max-tick-time","description",False,isInt=True))
settings.append(Setting("use-native-transport","description",False,isBool=True))
settings.append(Setting("max-players","description",True,isInt=True))
settings.append(Setting("online-mode","description",True,isBool=True))
settings.append(Setting("enable-status","description",True,isBool=True))
settings.append(Setting("allow-flight","description",True,isBool=True))
settings.append(Setting("broadcast-rcon-to-ops","description",False,isBool=True))
settings.append(Setting("view-distance","description",False,isInt=True))
settings.append(Setting("allow-nether","description",True,isBool=True))
settings.append(Setting("server-port","description",True,isInt=True))
settings.append(Setting("enable-rcon","description",False,isBool=True))
settings.append(Setting("sync-chunk-writes","description",False,isBool=True))
settings.append(Setting("op-permission-level","description",True,isInt=True))
settings.append(Setting("prevent-proxy-connections","description",True,isBool=True))
settings.append(Setting("resource-pack","description",True,isStr=True))
settings.append(Setting("entity-broadcast-range-percentage","description",True,isInt=True))
settings.append(Setting("rcon.password","description",True,isStr=True))
settings.append(Setting("player-idle-timeout","description",True,isInt=True))
settings.append(Setting("force-gamemode","description",True,isBool=True))
settings.append(Setting("rate-limit","description",False,isInt=True))
settings.append(Setting("hardcore","description",True,isBool=True))
settings.append(Setting("white-list","description",True,isBool=True))
settings.append(Setting("broadcast-console-to-ops","description",False,isBool=True))
settings.append(Setting("spawn-npcs","description",True,isBool=True))
settings.append(Setting("spawn-animals","description",True,isBool=True))
settings.append(Setting("snooper-enabled","description",False,isBool=True))
settings.append(Setting("function-permission-level","description",True,isInt=True))
settings.append(Setting("level-type","description",True,isStr=True))
settings.append(Setting("text-filtering-config","description",False,isStr=True))
settings.append(Setting("spawn-monsters","description",True,isBool=True))
settings.append(Setting("enforce-whitelist","description",True,isBool=True))
settings.append(Setting("resource-pack-sha1","description",True,isBool=True))
settings.append(Setting("spawn-protection","description",True,isInt=True))
settings.append(Setting("max-world-size","description",True,isInt=True))
settings.append(Setting("max-build-height","description",True,isInt=True))

def loadSettingInfos():

    global settingsInfoDict

    for key,value in settingsDict.items():

        for setting in settings:
            if(setting.key == key):
                settingInfo = SettingVal(setting,value)
                settingsInfoDict[key] = settingInfo
    
    