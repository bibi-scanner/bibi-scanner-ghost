from flask import request
import json
from os import path
import os
import importlib


def noticeTask():

    data = request.data
    data = json.loads(data)


    return "123"