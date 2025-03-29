import sys
from flask import Flask, render_template, request


#!/usr/bin/env python3

import argparse
import time
import threading

import sys
from os.path import dirname
#from pwn import *

from flask import Flask, request
from flask import render_template
from flask import render_template_string
import urllib



sys.path.append(dirname(__file__) + "/")  # NOTE: костыль для испорта jury_sdk
from jury_sdk.python_client import protocol, Jury  # noqa

app = Flask(__name__)
jury = Jury(None, None, True)

alph = "П2зоЙуМщВЁрЩКфчСОйцРБЖлНэжх0Уъя59ТЧЪаЮФв1ЕЯИсштЫнымгГьДдпюкАЗШ78ёЬе3ЭХЛЦ46би"
app.config.from_object(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Simple example")
    parser.add_argument("team_id", type=int, help="Team id for this instance")
    parser.add_argument("--ip_jury", type=str, help="ip addr jury", default="127.0.0.1")
    parser.add_argument("--port_jury", type=int, help="port addr jury", default=30555)
    return parser.parse_args()

cmd = parse_args()

def wait_unlock(jury, unlock_event, team_id):
    print("state =", jury.get_state(team_id))
    while jury.get_state(team_id) == protocol.State.LOCK:
        print("I need you to do somethind todo")
        unlock_event.wait(1)


def work_once(jury, team_id):
    app.run(host='0.0.0.0', debug=True)


 
@app.route("/")
def index():
    return render_template('/index.html')

@app.route("/api/flag", methods = ["POST"])
def flag():
    global cmd
    global jury
    flag = request.get_json()["text"]
    if flag != "flag{PudgeAndBase76DonePizdone}":
        jury.alert(cmd.team_id, sync=True)
        otv = "Time to drink!!!!"
        res={"answ":otv}
    else:
        otv = "YAAAAAY YOU WIN!!!"
        res={"answ":otv}
    return res
    
    

@app.route("/api/encode", methods = ["POST"])
def encode():
    global cmd
    global jury
    jury.alert(cmd.team_id, sync=True)
    arr = request.get_json()["text"]
    str = ""
    for i in arr:
        str += hex(int(i))[2:]
    b = str
    str = int(str, 16)
    c = str
    ost = []
    while True:
        ost.append(str%76)
        str //=76
        if str == 0:
            break
    ost.reverse()
    otv = ""
    for i in ost:
        otv += alph[i]
    otv = otv + "\n Time to drink!!!"
    res={"answ":otv}
    return res

def main():
    # cmd = parse_args()
    # jury = Jury(None, None, True)
    # NOTE: event используется тут просто для примера, его можно заменить на любую другую блокировку
    # как и вообще игнорировать состояния команд
    unlock_event = threading.Event()

    def finished():
        "Завершает общение и выходит из программы"
        jury.stop()
        sys.exit(0)
        print("Bye.")

    def set_state(team, state: protocol.State):
        "Оповещает через unlock_event"
        if state == protocol.State.UNLOCK:
            unlock_event.set()
        else:
            unlock_event.clear()

    jury.set_callbacks(set_state, finished)
    jury.start(cmd.ip_jury, cmd.port_jury, [cmd.team_id])

    while True:
        try:
            wait_unlock(jury, unlock_event, cmd.team_id)
            work_once(jury, cmd.team_id)
        except KeyboardInterrupt:
            finished()


if __name__ == "__main__":
    main()

