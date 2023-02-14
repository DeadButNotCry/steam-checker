import os

from checker.checker import cookie_check


def main():
    for filename in os.listdir("cookies"):
        res = cookie_check(filename)
        print("Cookie", res.works)

if __name__ == '__main__':
    main()

