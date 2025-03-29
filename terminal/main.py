#!/usr/bin/env python3

import argparse
import time
import threading

import sys
from os.path import dirname
from pwn import *

sys.path.append(dirname(__file__) + "/../../")  # NOTE: костыль для испорта jury_sdk
from jury_sdk.python_client import protocol, Jury  # noqa


def parse_args():
    parser = argparse.ArgumentParser(description="Simple example")
    parser.add_argument("team_id", type=int, help="Team id for this instance")
    parser.add_argument("--ip_jury", type=str, help="ip addr jury", default="127.0.0.1")
    parser.add_argument("--port_jury", type=int, help="port addr jury", default=30555)
    return parser.parse_args()


def wait_unlock(jury, unlock_event, team_id):
    print("state =", jury.get_state(team_id))
    while jury.get_state(team_id) == protocol.State.LOCK:
        print("I need you to do somethind todo")
        unlock_event.wait(1)


# def work_once(jury, team_id):
#     code = input("Enter a math expression: ")
#     ans = "you can't hack me!"
#     try:
#         res = eval(code)
#         if type(res) not in (int, float):
#             jury.alert(team_id, sync=True)
#         else:
#             ans = f"Your result: {res}"
#     except:  # noqa
#         jury.alert(team_id, sync=True)
#
#     print(ans)


def work_once(jury, team_id):
    l = listen(9999)
    svr = l.wait_for_connection()

    print(l.sendline(b"hello my friend it is my secret server"))
    print(l.sendline(b"we have several commands use help"))
    while (True):
        line = l.recvline().decode('utf-8')

        # print(line[:-1] == "ls")
        workline = line[:-1]
        if workline == "ls":
            l.sendline(b"ls is tired")
        elif workline == "help":
            l.sendline(b" comand is :\n ls\n cd\n drink\n getflag\n")
        elif workline == "cd":
            l.sendline(b"cd it is dificalt to me")
        elif workline == "getflag":
            while (True):
                l.sendline(b"you need to use binary search to find the flag")
                for i in range(1, 1000):
                    l.send((str(i) + " ").encode())
                while (True):
                    number = l.recvline().decode('utf-8')
                    if int(number[:-1]) < 88:
                        l.sendline(b"more\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
                    elif int(number[:-1]) > 88:
                        l.sendline(b"less\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
                    elif int(number[:-1]) == 88:
                        l.sendline(b"flag{blablabla}")
                        # обязательно залогировать флаг иначе будет не оч приятно
                    else:
                        l.sendline(b"error\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
        else:
            l.sendline(b"time to drink")
            # вставить блокировку
            jury.alert(team_id, sync=True)


def main():
    cmd = parse_args()
    jury = Jury(None, None, True)
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