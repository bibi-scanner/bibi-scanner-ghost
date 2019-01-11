import time
import requests
import json
from config import getConfig
from classes.ip2address import long2ip
from os import path

class Tasks:

    def __init__(self):
        self.runingTask = None

    def getRunningTask(self):
        return self.runingTask

    def startTask(self, task):
        if self.runingTask:
            return False

        self.runingTask = task
        task.runTask()
        return True

    def clearTask(self):
        self.runingTask = None

    def taskend(self):
        config = getConfig()
        r = requests.post(config["centerBaseURL"] + "/nodes/" + config["id"] + "/tasks/update")

        return ""

pluginsdir = path.abspath(path.join(path.dirname(__file__), "../plugins"))

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
    startPort = task["startPort"]
    endPort = task["endPort"]
    plugins = task["plugins"]

    for plugin in plugins:
        r = requests.get(config["centerBaseURL"] + "/plugins/" + plugin)
        plugindata = r.content
        f = open(path.join(pluginsdir, plugin + ".py"), "w", encoding="utf-8")
        f.write(plugindata.decode())
        f.close()

    task = Task(id, range, startPort, endPort, plugins)

    return task


globaltasks = Tasks()

