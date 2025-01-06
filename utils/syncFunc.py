import string
import random

from subprocess import Popen, PIPE
import os

from config import domain, dont_stop_list


class Password:

    # Store all characters in lists
    __letters_low = list(string.ascii_lowercase)
    __letters_up = list(string.ascii_uppercase)
    __digits = list(string.digits)

    def __new__(cls, length: int = 24) -> str:

        # Shuffle all lists
        random.shuffle(cls.__letters_low)
        random.shuffle(cls.__letters_up)
        random.shuffle(cls.__digits)

        # Calculate 30% & 20% of number of characters
        first_part = round(length * (30 / 100))
        second_part = round(length * (40 / 100))

        # Generation of the password (60% letters and 40% digits)
        result = []

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

    def __new__(cls, *, command: str, file: str, port: int, password: str) -> list[str]:
        return ["marimo", command, file, "-p", f"{port}", "--token-password", password]


class SSHCMD:

    def __new__(cls, *, port: int) -> list[str]:
        return ["ssh", "-R", f"{port}:localhost:{port}", domain]


def stop_subprocesses(*subprocesses: Popen) -> None:

    for sub in subprocesses:
        pid = sub.pid

        temp = Popen(f"ps -e | grep {pid}", shell=True, stdout=PIPE)
        p_name = str(temp.communicate()[0]).split()[4].replace(
            "\n", "").replace(
            "\\n", "").replace(
            "\\n'", "").replace(
            "'", ""
        )

        if p_name == "marimo":
            print("")

        os.system(f"kill {pid} STOP")

        if p_name not in dont_stop_list:
            temp = Popen(f"ps -e | grep {p_name}", shell=True, stdout=PIPE)
            result = temp.communicate()[0]

            if result and result != "":
                os.system(f"kill {str(result).split()[1]} STOP")
