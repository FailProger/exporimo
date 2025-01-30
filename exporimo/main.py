from subprocess import Popen, PIPE

import random

import os
from pathlib import Path

from .types import Password, MarimoCMD, ExposeCMD, ExporimoSession
from .params import ExposeService

from .utils import stop_subprocesses, _dont_kill_list


__all__ = (
    "Exporimo"
)


class Exporimo:

    __index_list = list(range(1000))
    __port_range = [5500, 12500]

    __default_dir = "Notes/"
    __default_wd = str(Path(__default_dir).absolute())

    __one_setup = True

    __running_session: dict[int, ExporimoSession] = {}

    @classmethod
    def start_marimo(
            cls,
            command: str,
            file: str,
            index: int = None,
            port: int = None,
            password: str = None,
            service: ExposeService = ExposeService.ssh,
            print_url: bool = True
    ) -> str:

        cls.__setup()

        file = file if file.endswith(".py") else f"{file}.py"
        index = cls.__index_list.pop(0) if index is None else index
        port = random.randint(cls.__port_range[0], cls.__port_range[1]) if port is None else port
        password = Password() if password is None else password

        url, marimo_popen, expose_popen = cls.__start(
            command=command,
            file=file,
            port=port,
            password=password,
            service=service
        )

        if print_url:
            print(f"Your url:\n{url}")

        cls.__running_session[index] = ExporimoSession(
            marimo_popen=marimo_popen,
            expose_popen=expose_popen,
            url=url
        )

        return url

    @classmethod
    def stop_marimo(cls, index: int = None) -> None:
        if index is None and len(cls.__running_session) == 1:
            index = 0

        elif index is None:
            raise ValueError("Enter session index")

        stop_subprocesses(
            cls.__running_session[index].marimo_popen,
            cls.__running_session[index].expose_popen
        )

    @classmethod
    def wait(cls, index: int = None, until_input: bool = True, stop_word: str = "stop") -> None:
        try:
            while True:
                if until_input and input() == stop_word:
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            cls.stop_marimo(index)

        except Exception:
            cls.stop_marimo(index)
            raise

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

    @classmethod
    def __setup(cls) -> None:
        if cls.__one_setup:
            cls.__check_def_dir()
            cls.__check_wd()

            cls.__one_setup = False

    @classmethod
    def __check_def_dir(cls) -> None:

        path = Path(cls.__default_dir).absolute()

        if not path.exists() or (path.exists() and not path.is_dir()):
            os.mkdir(f"{path}/")

    @classmethod
    def __check_wd(cls) -> None:
        temp = Popen(
            ["pwd"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        result = str(temp.communicate()[0])[2:][:-1][:-1][:-1]

        if result != cls.__default_wd:
            os.chdir(cls.__default_wd)
