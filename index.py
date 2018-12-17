from flask import Flask
import json
import requests
from classes.aescrpyto import AESCrpyto
from config import getConfig
import threading
from tasks import getRemoteTask, globaltasks

config = getConfig()


# 初始化注册
def pingcenter():
    c = AESCrpyto(config["key"])
    data = {
        "id": config["id"],
        "ip": config["ip"],
        "port": config["port"],
    }
    data = json.dumps(data)
    requests.post(config["centerBaseURL"] + "/nodes/registry", data)


# 初始化执行任务
def initRunTask():
    task = getRemoteTask()
    if task and not globaltasks.getRunningTask():
        globaltasks.startTask(task)


app = Flask(__name__)
app.debug = True


# PING
@app.route('/ping', methods=['POST'])
def ping():
    return "ok"


import interfaces.tasks as tasksInterfaces


# 通知任务
@app.route('/tasks', methods=['POST'])
def task():
    threading.Thread(target=initRunTask).start()
    return "ok"


# 查询节点任务进度
@app.route('/tasksinfo', methods=['GET'])
def tasksinfo():
    task = globaltasks.getRunningTask()

    tasks = []
    if task:
        tasks.append({
            "id": task.id,
            "progress": task.progress,
            "result": task.result
        })

    return json.dumps({
        "tasks": tasks
    })


# 完成任务
@app.route('/tasks/<taskId>/complete', methods=['POST'])
def taskComplete(taskId):
    task = globaltasks.getRunningTask()

    if task.id == taskId and task.progress == 1:
        globaltasks.clearTask()
        threading.Thread(target=initRunTask).start()

    return "ok"


if __name__ == '__main__':
    threading.Thread(target=pingcenter).start()
    threading.Thread(target=initRunTask).start()
    app.run(port=config["port"])
