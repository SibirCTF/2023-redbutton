import socket
import threading
from datetime import datetime
from typing import List, Dict
from .. import protocol


class Jury:
    """ Класс, реализующий коммуникацию между сервисом и жюррейкой.  
    Приём сообщений происходит в другом потоке, после обработки вызывается  
    конкретный 'сервисный' обработчик - асинхронная обработка.
    """  # noqa

    class StateTeam:
        """
        Внутреннее представление состояния команды.
        set_state_event используется для синхронной обработки.
        """
        def __init__(self):
            self.set_state_event = threading.Event()
            self.protcol_state = None

    def __init__(self, set_status_callback, finished_callback, debug_log=False):
        self._set_status_callback = None
        self._finished_callback = None
        self._debug_log = debug_log

        self._jury_socket = None
        self._has_stop = False
        self._thread_recv = None
        self._state_teams = {}  # type: Dict[int, Jury.StateTeam]

        self.set_callbacks(set_status_callback, finished_callback)

    def set_callbacks(self, set_status_callback, finished_callback):
        """
        Установить callback'b для метода
        """
        self._set_status_callback = set_status_callback
        self._finished_callback = finished_callback

    def alert(self, team_id: int, sync=False, timeout=None):
        """
        Отправить алерт для команды.
        При sync = False метод ничего не возвращает.
        При sync = True метод ожидает ответ журейки и возвращает состояние.
        """
        if not self.__has_connect():
            raise RuntimeError("No connection to juraci")

        dt = datetime.now()
        data = (protocol.Protocol.alert(team_id, dt) + '\n').encode()
        # self.__print(">", data)
        self._jury_socket.send(data)
        if sync:
            return self.__wait_state_of(team_id, timeout)

    def state_request(self, team_id: int, sync=True, timeout=None):
        """
        Отправить запрос состояния, ответ будет дан через обработчик set_state
        Если флаг 'sync' будет выставлен, то вернётся и тут
        """
        if not self.__has_connect():
            raise RuntimeError("No connection to juraci")

        if team_id not in self._state_teams:
            raise RuntimeError("Team not found")

        data = (protocol.Protocol.state_request(team_id) + '\n').encode()
        # self.__print(">", data)
        self._jury_socket.send(data)
        if sync:
            return self.__wait_state_of(team_id, timeout)

    def get_state(self, team_id: int):
        """
        Вернуть сохранённое состояние команды.
        """

        if team_id not in self._state_teams:
            raise RuntimeError("Team not found")

        return self._state_teams[team_id].protcol_state

    def start(self, ip, port, teams: List[int]):
        """
        Старт общения, отложенный старт.
        Ждёт пока состояние всех команд проинициализируется
        """
        self._has_stop = False

        self._jury_socket = socket.socket()
        self._jury_socket.connect((ip, port))
        self._thread_recv = threading.Thread(target=self.__recv, name="ClientJury recv")
        self._thread_recv.start()

        for t_id in teams:
            self._state_teams[t_id] = Jury.StateTeam()
            self._state_teams[t_id].set_state_event.clear()
            self.state_request(t_id, sync=False)

        for _, st in self._state_teams.items():
            st.set_state_event.wait()  # TODO: а что с timeout?

    def stop(self):
        """
        Мягко остановить общение
        """
        self._has_stop = True

        Jury.__wrap_shutdown(self._jury_socket)
        self._thread_recv = None

    def __wait_state_of(self, team_id, timeout):
        self._state_teams[team_id].set_state_event.clear()
        self._state_teams[team_id].set_state_event.wait(timeout)
        return self._state_teams[team_id].protcol_state  # TODO: мб через get_state?

    def __recv(self):
        # self._jury_socket.settimeout(5)
        while not self._has_stop:
            try:
                data = self._jury_socket.recv(1024)

                if data is None or len(data) == 0:
                    self.__print("[Jury]: jury lost")
                    break

                for part in data.decode().splitlines():
                    # self.__print("<", data)
                    try:
                        obj = protocol.Protocol.parse(part)
                        self.__route_callbacks(obj)
                    except Exception as e:
                        self.__print(f"[Jury]: exception: {e}")

            except socket.timeout:
                pass
            except OSError:  # raise on .shutdown()
                pass
            except Exception as e:
                self.__print(f"[Jury]: exception: {e}")

    def __has_connect(self):
        # TODO: добавить другие проверки
        return self._jury_socket is not None

    def __set_state(self, obj):
        self._state_teams[obj["team"]].protcol_state = obj["state"]
        self._state_teams[obj["team"]].set_state_event.set()  # NOTE: .clear вызывется тогда, когда код хочет синхронно ждать

        if self._set_status_callback is not None:
            self._set_status_callback(team=obj["team"], state=obj["state"])
        else:
            self.__print(f"[Jury]: income set_state ({obj}), but callback is not set")

    def __finished(self, obj):
        if self._finished_callback is not None:
            self._finished_callback()
        else:
            self.__print(f"[Jury]: income finished ({obj}), but callback is not set")
        # self.stop()

    def __route_callbacks(self, obj: dict):
        if obj["method"] == protocol.Method.SET_STATE:
            self.__set_state(obj)
        elif obj["method"] == protocol.Method.FINISHED:
            self.__finished(obj)
        # TODO: добавить ERROR
        else:
            self.__print(f"[Jury]: income {obj['method']} ({obj}), but client does not route this method")

    @staticmethod
    def __wrap_shutdown(soc: socket.socket, how=socket.SHUT_RDWR):
        try:
            soc.shutdown(how)
        except:  # noqa
            pass

    def __print(self, *args, **kwargs):
        if self._debug_log:
            print(*args, **kwargs)
