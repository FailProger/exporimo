import os
from logging import Logger, Handler, INFO, StreamHandler, FileHandler, getLogger, basicConfig
from pathlib import Path
from typing import Iterable


# Path to logs
class LogsFile:
    """Class of logs files"""

    def __init__(self, file_name: str, folder_path: str):
        self.folder_path = folder_path
        self.file_path = file_name

    @property
    def folder_path(self) -> Path:
        return self.__folder_path

    @folder_path.setter
    def folder_path(self, folder_path: str) -> None:
        folder = Path(f"{folder_path}").absolute()

        if not os.path.exists(folder):
            os.makedirs(folder)

        self.__folder_path = folder

    @property
    def file_path(self) -> Path:
        return self.__file_path

    @file_path.setter
    def file_path(self, file_name: str) -> None:
        self.__file_path = Path(f"{self.__folder_path}/{file_name}.txt").absolute()


class MainLogger:
    # Logs format
    __default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s: %(lineno)d)"

    def __new__(
            cls,
            loger_name: str = "main",
            file_name: str = "main_logs",
            folder_path: str | None = ".logs",
            write_mode: str = "a",
            level: int = INFO,
            format: str = __default_format,
            encoding: str = "UTF-8",
            add_handlers: Iterable[Handler] = None,
            turn_off: bool = False,
            **kwargs
    ) -> Logger:

        if folder_path is None:
            folder_path = ""

        logs_file = LogsFile(file_name, folder_path)

        # Logs handlers
        sh = StreamHandler()
        fh = FileHandler(filename=logs_file.file_path, mode=write_mode, encoding=encoding)

        handlers = [sh, fh]

        if add_handlers:
            handlers.append(*add_handlers)

        if turn_off:
            handlers = []

        # Logs config
        basicConfig(level=level, format=format, handlers=handlers, **kwargs)

        return getLogger(loger_name)
