#!/usr/bin/env python3
import argparse
import time
import threading
import sys
from os.path import dirname
from pwn import *

sys.path.append(dirname(__file__) + "/")  # NOTE: костыль для испорта jury_sdk
from jury_sdk.python_client import protocol, Jury  # noqa


def parse_args():
    parser = argparse.ArgumentParser(description="Simple example")
    parser.add_argument("team_id", type=int, help="Team id for this instance")
    parser.add_argument("--ip_jury", type=str, help="ip addr jury", default="127.0.0.1")
    parser.add_argument("--port_jury", type=int, help="port addr jury", default=30555)
    return parser.parse_args()


def wait_unlock(jury, unlock_event, team_id):

    while jury.get_state(team_id) == protocol.State.LOCK:
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
    s = server(4444)
    while(True):
        server_conn = s.next_connection()
        server_conn.sendline(b"hello my friend in new osint task\nwhere is this muzhik standing?\n https://drive.google.com/file/d/1EQasJFDujaLIZJh-T3lbsdb4fU61zrV_/view?usp=sharing")
    #нужна ссылка на фото выложенное на google disk
        server_conn.sendline(b"we have several commands use help: \nhints\n drink\nputflag\n")
        while(True):
            try:
                line= server_conn.recvline().decode('utf-8')
                workline = line[:-1]

                if workline =="help":
                    server_conn.sendline(b" comand is :\n hints\n drink\n putflag\n")

                elif workline == "putflag":
                    server_conn.sendline(b"give me flag")
                    flag=server_conn.recvline().decode('utf-8')
                    if flag == "flag{refer_to_Atomic_Heart}":
                        server_conn.sendline(b"You WIN!")
                    else:
                        server_conn.sendline(b"You Loose!")
                        jury.alert(team_id, sync=True)

                elif workline == "hints":
                    while(True):
                        server_conn.sendline(b"We have 6 hint for you. Give number hint please!")
                        for i in range(1,7):
                            server_conn.sendline((str(i)+" ").encode())
                        while(True):
                            server_conn.sendline(b"\n your number > ")
                            number=int(server_conn.recvline().decode('utf-8'))
                            if number ==1:
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                                server_conn.sendline(b"It is located in Seversk")
                            elif number ==2:
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                                server_conn.sendline(b"Located on Communist Avenue")
                            elif number ==3:  
                                server_conn.sendline(b"Near house number 51")
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                            elif number ==4:  
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                                server_conn.sendline(b"https://www.youtube.com/watch?v=wpExy1AmZ-8")
                            elif number ==5:  
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                                server_conn.sendline(b"The flag is on Google map")
                            elif number ==6:  
                                server_conn.sendline(b"time to drink!\n")
                                jury.alert(team_id, sync=True)
                                server_conn.sendline(b"There are no more hints, but you can check the flag using putflag")
                            else:
                                server_conn.sendline(b"wrong number\n time to drink\n")
                                jury.alert(team_id, sync=True)
                else:
                    server_conn.sendline(b"time to drink")
                    jury.alert(team_id, sync=True)
            except:
                pass

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
