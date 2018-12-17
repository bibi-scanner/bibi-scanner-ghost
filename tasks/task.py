import threading
import time
from tasks import globaltasks

class Task:

    def __init__(self, id, range, plugins):
        self.id = id
        self.range = range
        self.plugins = plugins
        self.progress = 0
        self.result = None

    def run(self):
        threading.Thread(target=self.runTask, args=[]).start()

    def end(self):
        globaltasks.taskend()
        return ""

    def runTask(self):
        while 1:
            time.sleep(1)
            self.progress += 0.25
            print(self.id + ":" + str(self.progress))
            if self.progress >= 1:
                self.progress = 1

                self.result = {
                    "numberOfHosts": 1,
                    "numberOfPorts": 2,
                    "numberOfWarnings": 1,
                    "hosts":[
                        {
                            "host": "127.0.0.1",
                            "numberOfPorts": 2,
                            "numberOfWarnings": 1,
                            "ports": [
                                {
                                    "port": 3000,
                                    "numberOfWarnings": 1,
                                    "warnings": [
                                        {
                                            "description": "哈哈哈哈",
                                            "plugin": "1e1d0930-d0e5-4f02-9a77-92ad587cf097"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }

                self.end()
                break
