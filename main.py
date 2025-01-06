from subprocess import Popen, PIPE
import random

from utils.syncFunc import Password, MarimoCMD, SSHCMD, stop_subprocesses
from config import domain


port_range = [5500, 12500]


def start_marimo(command: str, file: str, port: int, password: str):

    marimo_cmd = MarimoCMD(
        command=command,
        file=file,
        port=port,
        password=password
    )
    ssh_cmd = SSHCMD(
        port=port
    )

    marimo = Popen(marimo_cmd, stdout=PIPE)
    ssh = Popen(ssh_cmd, stdout=PIPE)

    try:
        marimo.wait()
        ssh.wait()

    except:
        stop_subprocesses(marimo, ssh)


def main():

    port = random.randint(port_range[0], port_range[1])
    password = Password()

    url = f"http://{domain}:{port}?access_token={password}"
    print(url)

    start_marimo("edit", "test.py", port, password)


if __name__ == '__main__':
    main()
