from subprocess import Popen, PIPE

import random

from pybook.types import Password, MarimoCMD, ExposeCMD, PyBookSession
from pybook.params import ExposeService

from pybook.utils import stop_subprocesses, _dont_kill_list


__all__ = (
    "PyBook"
)


class PyBook:

    __port_range = [5500, 12500]

    __running_session: dict[int, PyBookSession] = {}

    @classmethod
    def start_marimo(
            cls,
            tg_id: int,
            command: str,
            file: str,
            port: int | None = None,
            password: str | None = None,
            service: ExposeService = ExposeService.ssh
    ) -> str:

        port = random.randint(cls.__port_range[0], cls.__port_range[1]) if port is None else port
        password = Password() if password is None else password

        url, marimo_popen, expose_popen = cls.__start(
            command=command,
            file=file,
            port=port,
            password=password,
            service=service
        )

        cls.__running_session[tg_id] = PyBookSession(
            marimo_popen=marimo_popen,
            expose_popen=expose_popen,
            url=url
        )

        return url

    @classmethod
    def stop_marimo(cls, tg_id: int) -> None:
        stop_subprocesses(
            cls.__running_session[tg_id].marimo_popen,
            cls.__running_session[tg_id].expose_popen
        )

    @classmethod
    def set_port_range(cls, start: int, end: int) -> None:
        cls.__port_range[0] = start
        cls.__port_range[1] = end

    @staticmethod
    def dont_stop_serves(serves_name: str) -> None:
        _dont_kill_list.append(serves_name)

    @classmethod
    def __start(
            cls,
            *,
            command: str,
            file: str,
            port: int,
            password: str,
            service: ExposeService
    ) -> tuple[str, Popen, Popen]:

        marimo_cmd = MarimoCMD(
            command=command,
            file=file,
            port=port,
            password=password
        )
        expose_cmd, url = ExposeCMD(
            service=service,
            port=port,
            password=password
        )

        marimo_popen = Popen(marimo_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        expose_popen = Popen(expose_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        return url, marimo_popen, expose_popen
