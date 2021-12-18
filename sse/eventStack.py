
import time

import flask


eventStackHandler = None

def getEventStackHandler():
    global eventStackHandler
    if eventStackHandler == None:
        eventStackHandler = EventStackHandler()
    return eventStackHandler


class EventStackHandler:

    eventStack = None

    running = False
    running_paused = False
    interrupt = False

    last_message = ""

    generator = None
    
    def __init__(self) -> None:
        self.eventStack = ["",""]
        pass

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def hasNext(self):
        if len(self.eventStack) > 0:
            return True
        return False

    def addEvent(self,event):

        self.eventStack.append(event)
        self.last_message = event
        print(self.eventStack)

    def getGenerator(self):
        
        if self.generator == None:
            self.generator = self.run()

        return self.generator

    def run(self):
        while self.running:
            time.sleep(1)
            if self.hasNext():
                data = self.eventStack.pop(0)
                print(data)
                yield f"data: {data}\n\n"

class EventStack(list):

    def __init__(self) -> None:
        pass