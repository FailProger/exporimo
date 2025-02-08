import string
import random

from subprocess import Popen, PIPE


__all__ = (
    "stop_subprocesses",
    "Password"
)


_dont_kill_list = ["ssh-agent"]


def stop_subprocesses(*subprocesses: Popen) -> None:
    for sub in subprocesses:
        pid = sub.pid

        temp = Popen(f"ps -e | grep {pid}", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result_split = str(temp.communicate()[0]).split()

        if len(result_split) > 4:
            p_name = result_split[4].replace(
                "\n", "").replace(
                "\\n", "").replace(
                "\\n'", "").replace(
                "'", ""
            )

            temp = Popen(["kill", f"{pid}", "STOP"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            temp.wait()

            temp = Popen(f"ps -e | grep {p_name}", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            result = str(temp.communicate()[0])[2:][:-1]

            if result and result != "":
                for line in result.split("\\n"):
                    line_split = line.split()

                    if line_split and line_split[3] not in _dont_kill_list:
                        temp = Popen(
                            [f"kill", f"{line_split[0]}", "STOP"], stdin=PIPE, stdout=PIPE, stderr=PIPE
                        )
                        temp.wait()


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
