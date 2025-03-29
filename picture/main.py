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
    app.run(debug=True, host='0.0.0.0',port=5000)
   

@app.route('/')
def hello_world():
    #return '<img src="https://hi-news.ru/wp-content/uploads/2017/12/maxresdefault-2.jpg" width="800" height="700"" align="middle">'
    return render_template('index.html')




@app.route('/@!ZKBf3jGWrtK9M6zILxwGv__0tf5eCaSod6eSJX1tyn0XnHji')
def hello():
    return 'flag{DataVas1aAl1en1sCool3517tipa}'


##в этой функции проблема

@app.errorhandler(404)
def page_not_found(error):
    error_text = '''
    <h1>Time To Drink!</h1>
    ''' 
    #вставить блокировку)))
    global cmd
    global jury
    jury.alert(cmd.team_id, sync=True)
    return render_template_string(error_text)
   

    


    

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