from subprocess import Popen, PIPE


__all__ = (
    "stop_subprocesses"
)


_dont_kill_list = ["ssh-agent"]


def stop_subprocesses(*subprocesses: Popen) -> None:
    for sub in subprocesses:
        pid = sub.pid

        temp = Popen(f"ps -e | grep {pid}", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p_name = str(temp.communicate()[0]).split()[4].replace(
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
