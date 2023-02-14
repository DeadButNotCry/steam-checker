import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from Models.Account import Account
from checker.netscape_loader import normal_format


def cookie_check(file_name):
    # print(file_name)
    f = open(f"cookies/{file_name}", "r")
    cookie = f.read()
    cookies = normal_format(cookie)
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Refer": "https://steamcommunity.com/",
        "Host": "store.steampowered.com"
    }
    resp = requests.get("https://store.steampowered.com/account/", headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    steam_id = soup.find(class_="youraccount_steamid")
    acc = Account()
    if steam_id is None:
        acc.works = False
        return acc
    acc.works = True

    return acc
