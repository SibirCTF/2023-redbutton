import re
from enum import Enum
from datetime import datetime


class State(Enum):
    """Возможные состояния сервиса"""
    LOCK = 0
    UNLOCK = 1


class Method(Enum):
    """Методов в протоколе"""
    STATE_REQUEST = 0
    SET_STATE = 1
    ALERT = 2
    ERROR = 3
    FINISHED = 4


class ErrorCode(Enum):
    """Возможные ошибки"""
    BAD_REQUEST = 401
    FORBIDDEN = 403
    INTERNAL_ERROR = 501


class ProtocolError(Exception):
    def __init__(self, code, what=""):
        super().__init__(what)
        self.code = code


class Protocol():
    """Утилитарный класс сериализации/десериализации протокола"""

    @staticmethod
    def state_request(team: int) -> str:
        """Сформировать метод STATE_REQUEST с данными"""
        method = Method.STATE_REQUEST.name
        return f"{method}: {team}"

    @staticmethod
    def alert(team: int, timestamp: datetime) -> str:
        """Сформировать ALERT с данными"""
        method = Method.ALERT.name
        posix = timestamp.timestamp()
        return f"{method}: {team} {posix}"

    @staticmethod
    def set_state(team: int, state: State) -> str:
        """Сформировать SET_STATE с данными"""
        method = Method.SET_STATE.name
        return f"{method}: {team} {state.name}"

    @staticmethod
    def finished() -> str:
        """Сформировать FINISHED"""
        method = Method.FINISHED.name
        return f"{method}"

    @staticmethod
    def error(code: ErrorCode, description: str = "") -> str:
        """Сформировать ERROR с кодом и описанием"""
        method = Method.ERROR.name
        return f"{method}: {code.value} {description}"

    @staticmethod
    def parse(message: str) -> dict:
        res = re.split(r'[:\s]+', message)

        method = Method[res[0]]

        data = {
            'method': method
        }

        if method == Method.STATE_REQUEST:
            data['team'] = int(res[1])
        elif method == Method.SET_STATE:
            data['team'] = int(res[1])
            data['state'] = State[res[2]]
        elif method == Method.ALERT:
            data['team'] = int(res[1])
            data['timestamp'] = datetime.fromtimestamp(float(res[2]))
        elif method == Method.ERROR:
            data['code'] = ErrorCode(int(res[1]))
            data['description'] = ""
            if len(res) > 2:
                data['description'] = res[2]
        elif method == Method.FINISHED:
            pass
        else:
            raise ProtocolError(ErrorCode.BAD_REQUEST, "Unknown method")

        return data
