import os

from bot.bot import bot_start
from checker.checker import cookie_check, start_checking
from init import init


def main():
    bot_start()


if __name__ == '__main__':
    init()
    main()
