from enum import Enum, auto


class ExposeService(Enum):
    """
    Services for expose marimo to Internet.\n
    :code:`SSH` mode use ssh for connect to :code:`serveo.net` or :code:`localhost.run` and expose marimo.

    Note:
        For using :code:`localtunnel` you must install it.
        More about on https://github.com/localtunnel/localtunnel
    """

    local_network = auto()
    ssh = auto()
