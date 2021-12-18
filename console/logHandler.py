from posix import listdir
import re
from flask_login.utils import login_required
from serverInfo import serverPath
import os

logHandler = None

def getLogHandler():
    
    global logHandler

    if logHandler == None:
        logHandler = LogHandler()

    return logHandler

class LogHandler():

    logPath = ""

    def __init__(self) -> None:
        self.logPath = f"{serverPath}/logs/latest.log"

    def getAll(self):
        
        content = ""

        with open(self.logPath,"r") as f:
            content = f.read()
        
        return content

    def getLines(self, lineCount:int):

        lines = []

        with open(self.logPath,"rb") as f:
            
            f.seek(0,os.SEEK_END)

            buffer = bytearray()

            pointer = f.tell()

            while pointer >= 0:

                f.seek(pointer)

                pointer = pointer - 1

                new_Byte = f.read(1)

                if new_Byte == b'\n':
                    lines.append(buffer.decode()[::-1])
                    buffer = bytearray()
                    if(len(lines) == lineCount):
                        return list(reversed(lines))
                else:
                    buffer.extend(new_Byte)
            
            if len(buffer) > 0:
                lines.append(buffer.decode()[::-1])

        return list(reversed(lines))