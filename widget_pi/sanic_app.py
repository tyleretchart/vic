import os
import sys
import signal
import psutil
import logging

from sanic import Sanic
from sanic.response import json
from multiprocessing import Process

# for the widgets
import time
from gpiozero import LED

#
# -------------------------------------------------
# helpers


def execute_string(s):
    exec(s)


def signal_handler(signal, frame):
    pid = 1
    while pid != 0:
        try:
            pid = os.waitpid(-1, os.WNOHANG)[0]
            print(pid)
        except ChildProcessError as e:
            pid = 0


#
# -------------------------------------------------
# globals

app = Sanic()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()

#
# -------------------------------------------------
# sanic endpoints


@app.route(
    '/start', methods=[
        "POST",
    ])
async def start(request):
    try:
        code = request.form.get("code")
        p = Process(target=execute_string, args=(code, ))
        p.start()
        return json({"error": False, "msg": p.pid})
    except Exception as e:
        logger.warning("EXCEPTION: {}".format(e))
        return json({"error": True, "msg": str(e)})


@app.route('/kill_all')
async def kill_all(request):
    try:
        for child in psutil.Process().children():
            os.kill(child.pid, signal.SIGKILL)
            logger.info("CHILD KILLED: {}".format(child))
        return json({"error": False, "msg": ""})
    except Exception as e:
        logger.warning("EXCEPTION: {}".format(e))
        return json({"error": True, "msg": str(e)})


#
# -------------------------------------------------
# main

if __name__ == '__main__':
    signal.signal(signal.SIGCHLD, signal_handler)
    app.run(host='0.0.0.0', port=8000)
