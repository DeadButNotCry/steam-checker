import os

from checker.checker import cookie_check
from init import init


def main():
    for filename in os.listdir("cookies"):
        res = cookie_check(filename)
        print("Cookie", str(res))

if __name__ == '__main__':
    init()
    main()

