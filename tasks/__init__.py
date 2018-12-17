import time
import requests
import json
from config import getConfig
from classes.ip2address import long2ip

class Tasks:

    def __init__(self):
        self.runingTask = None

    def getRunningTask(self):
        return self.runingTask

    def startTask(self, task):
        if self.runingTask:
            return False

        self.runingTask = task
        task.run()
        return True

    def clearTask(self):
        self.runingTask = None

    def taskend(self):
        config = getConfig()
        r = requests.post(config["centerBaseURL"] + "/nodes/" + config["id"] + "/tasks/update")

        return ""

def getRemoteTask():
    from tasks.task import Task
    config = getConfig()

    r = requests.get(config["centerBaseURL"] + "/nodes/" + config["id"] + "/tasks")
    data = json.loads(r.content)
    tasks = data["tasks"]
    nexttask = None
    for task in tasks:
        if task["status"] < 2:
            nexttask = task

    task = nexttask

    if not task:
        return None

    id = task["id"]
    range = long2ip(task["startIP"]) + "-" + long2ip(task["endIP"])
    if task["startIP"] == task["endIP"]:
        range = long2ip(task["startIP"])
    plugins = task["plugins"]

    task = Task(id, range, plugins)

    return task


globaltasks = Tasks()

