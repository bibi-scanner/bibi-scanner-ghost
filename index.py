from flask import Flask
import json
import requests
from classes.aescrpyto import AESCrpyto
from config import getConfig
import threading

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


app = Flask(__name__)
app.debug = True

# PING
@app.route('/ping', methods=['POST'])
def ping():
    return "ok"

# 通知任务
@app.route('/task', methods=['POST'])
def ping():
    return "ok"

if __name__ == '__main__':
    threading.Thread(target=pingcenter).start()
    app.run(port=config["port"])



