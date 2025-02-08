from subprocess import Popen, PIPE

import random

import os
from pathlib import Path
from typing import Union

from .types import CMDs, ExporimoSession
from .params import ExposeService

from .utils import Password, stop_subprocesses, _dont_kill_list


__all__ = (
    "Exporimo"
)


class Exporimo:

    __index_list = list(range(1000))
    __port_range = [5500, 12500]

    __default_dir = "Notebooks/"
    __default_wd_path = Path(__default_dir).absolute()

    __running_session: dict[int, ExporimoSession] = {}

    @classmethod
    def start_marimo(
            cls,
            command: str,
            file: Union[str, Path],
            index: int = None,
            port: int = None,
            password: str = None,
            service: ExposeService = ExposeService.ssh,
            print_url: bool = True
    ) -> str:

        if index:
            url = cls.is_running(index)
            if url:
                return url

        file = cls.__check_file(file)
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
    def is_running(cls, index: int) -> Union[str, None]:
        if index in list(cls.__running_session.keys()):
            return cls.__running_session[index].url

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

        marimo_cmd, expose_cmd, url = CMDs(
            command=command,
            file=file,
            port=port,
            password=password,
            service=service
        )

        marimo_popen = Popen(marimo_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        expose_popen = Popen(expose_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        return url, marimo_popen, expose_popen

    @classmethod
    def __check_file(cls, file: Union[str, Path]) -> str:

        if type(file) is Path or Path(file).absolute().is_file():
            file = str(Path(file).absolute())

        else:
            cls.__create_default_dir()
            cls.__change_wd()

            file = str(file) if str(file).endswith(".py") else f"{file}.py"

        return file

    @classmethod
    def __create_default_dir(cls) -> None:
        if not cls.__default_wd_path.is_dir():
            os.mkdir(f"{cls.__default_wd_path}/")

    @classmethod
    def __change_wd(cls) -> None:
        temp = Popen(
            ["pwd"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        result = str(temp.communicate()[0])[2:][:-1][:-1][:-1]

        if result != str(cls.__default_wd_path):
            os.chdir(str(cls.__default_wd_path))
