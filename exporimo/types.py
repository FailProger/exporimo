import string
import random

from subprocess import Popen, PIPE, TimeoutExpired

from typing import NamedTuple

from .params import ExposeService
from .utils import stop_subprocesses


__all__ = (
    "Password",
    "MarimoCMD",
    "ExposeCMD",
    "ExporimoSession",
)


class ExporimoSession(NamedTuple):
    marimo_popen: Popen
    expose_popen: Popen
    url: str


class Password:

    # Store all characters in lists
    __letters_low: list[str] = list(string.ascii_lowercase)
    __letters_up: list[str] = list(string.ascii_uppercase)
    __digits: list[str] = list(string.digits)

    def __new__(cls, length: int = 24) -> str:

        # Shuffle all lists
        random.shuffle(cls.__letters_low)
        random.shuffle(cls.__letters_up)
        random.shuffle(cls.__digits)

        # Calculate 30% & 20% of number of characters
        first_part = round(length * (30 / 100))
        second_part = round(length * (40 / 100))

        # Generation of the password (60% letters and 40% digits)
        result: list[str] = []

        for x in range(first_part):
            result.append(cls.__letters_low[x])
            result.append(cls.__letters_up[x])

        for x in range(second_part):
            result.append(cls.__digits[x])

        # Shuffle result
        random.shuffle(result)

        # Join result
        password = "".join(result)

        return password


class MarimoCMD:

    def __new__(cls, command: str, file: str, port: int, password: str) -> list[str]:
        return ["marimo", command, file, "-p", f"{port}", "--token-password", password]


class SSHCMD:

    service_dict = {
        "serveo.net": "serveo.net",
        "localhost.run": "nokey@localhost.run"
    }

    def __init__(self):
        self.__domain = None

    def __call__ (self, port: int) -> list[str]:
        service = self.__available_service(port)
        return service

    @property
    def domain(self) -> str:
        return self.__domain

    def __available_service(self, port: int) -> list[str]:
        cmd_list = []

        for service in self.service_dict.values():
            cmd_list.append(
                ["ssh", "-R", f"{port}:localhost:{port}", service]
            )

        available_list: list[bool] = []

        for cmd in cmd_list:
            result = self.__check(cmd)
            available_list.append(result)

        if True in available_list:
            index = available_list.index(True)
            self.__domain = list(self.service_dict.keys())[index]
            return cmd_list[index]

        raise RuntimeError("All services is not available")

    @classmethod
    def __check(cls, cmd: list[str]) -> bool:
        popen = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        try:
            popen.communicate(timeout=0.5)
            stop_subprocesses(popen)
            return False

        except TimeoutExpired:
            stop_subprocesses(popen)
            return True


class ExposeCMD:

    def __new__(cls, service: ExposeService, port: int, password: str) -> tuple[list[str], str]:
        if service == ExposeService.ssh:
            ssh_cmd = SSHCMD()
            expose_cmd = ssh_cmd(port=port)

            host = f"{ssh_cmd.domain}:{port}"

        else:
            raise ValueError("Another services now not supported")

        return expose_cmd, cls.__url(host, password)

    @classmethod
    def __url(cls, host: str, password: str) -> str:
        return f"http://{host}?access_token={password}"
