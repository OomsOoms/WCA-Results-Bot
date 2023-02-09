# Init file for all commands

# from file name import init_function
from .profile_cmd import init_profile_cmd
from .test import testrr


def init_cmds(bot):
    init_profile_cmd(bot)
    testrr(bot)

