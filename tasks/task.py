import threading
import time
from tasks import globaltasks
from deal_all_infor.scanf_all import scanTask
import random

class Task(scanTask):

    def end(self):
        globaltasks.taskend()
        return ""

    def runTask(self):
        threading.Thread(target=self.run, args=[]).start()
