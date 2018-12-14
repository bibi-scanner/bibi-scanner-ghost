import threading
import time

class Tasks:

    def __init__(self):
        self.tasks = []

    def appendTask(self, task):
        self.tasks.append(task)

    def getTaskById(self, taskId):
        for task in self.tasks:
            if task.id == taskId:
                return task
        return None

    def deleteTaskById(self, taskId):
        for index in range(len(self.tasks)):
            if self.tasks[index].id == taskId:
                del self.tasks[index]
                return

def runTask(task):
    while 1:
        time.sleep(3)
        task.progress += 0.1
        if task.progress >= 1:
            task.progress = 1
            break


class Task:

    def __init__(self, id, startIP, endIP, plugins):
        self.id = id
        self.startIP = startIP
        self.endIP = endIP
        self.plugins = plugins
        self.progress = 0

    def run(self):
        threading.Thread(target=runTask, args=[task]).start()

task = Task("xxx", 0, 1, [])
task.run()
while 1:
    print(task.progress)
    if task.progress == 1:
        break
    time.sleep(1)