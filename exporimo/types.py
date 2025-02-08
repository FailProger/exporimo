from subprocess import Popen, PIPE, TimeoutExpired
from netifaces import interfaces, ifaddresses, AF_INET

from typing import NamedTuple

from .params import ExposeService
from .utils import stop_subprocesses


__all__ = (
    "ExporimoSession",
    "CMDs"
)


class ExporimoSession(NamedTuple):
    marimo_popen: Popen
    expose_popen: Popen
    url: str


class MarimoCMD:

    def __new__(cls, command: str, file: str, port: int, password: str, host: str = None) -> list[str]:
        cmd = ["marimo", command, file, "-p", f"{port}", "--token-password", password]

        if host:
            cmd.append("--host")
            cmd.append(str(host))

        return cmd


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

    __not_ifaces = ["lo", "loop"]

    def __new__(cls, port: int, service: ExposeService) -> tuple[list[str], str, int]:

        if service == ExposeService.ssh:
            ssh_cmd = SSHCMD()
            expose_cmd = ssh_cmd(port)
            host = str(ssh_cmd.domain)

        elif service == ExposeService.local_network:
            expose_cmd = ["clear"]

            host = None

            for iface_name in interfaces():
                if iface_name not in cls.__not_ifaces:
                    host = ifaddresses(iface_name).setdefault(AF_INET)[0]["addr"]
                    break

            if host is None:
                raise RuntimeError("Interfaces not found")

        else:
            raise ValueError("Another services now not supported")

        return expose_cmd, host, port


class CMDs:

    def __new__(
            cls,
            command: str,
            file: str,
            port: int,
            password: str,
            service: ExposeService
    ) -> tuple[list[str], list[str], str]:

        expose_cmd, host, expose_port = ExposeCMD(
            port=port,
            service=service
        )

        marimo_cmd = MarimoCMD(
            command=command,
            file=file,
            port=port,
            password=password,
            host=host if service == ExposeService.local_network else None
        )

        return marimo_cmd, expose_cmd, cls.__url(host, expose_port, password)

    @classmethod
    def __url(cls, host: str, port: int, password: str) -> str:
        return f"http://{host}:{port}?access_token={password}"
