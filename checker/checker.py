import sqlite3
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from Models.Account import Account
from checker.netscape_loader import normal_format
import lxml.html


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
    id = steam_id.text.split(" ")[2]
    acc.id = id
    # Check for duplicates
    con = sqlite3.connect("duplicate.db")
    res_from_db = con.execute("SELECT * FROM duplicates WHERE id=?",(id,))
    id_from_db = res_from_db.fetchone()
    if id_from_db is not None:
        acc.duplicate = True
        con.close()
        print(acc.duplicate)
        return acc
    else:
         acc.duplicate = False
         print(acc.duplicate)
         #TODO: save new acc to db
         con.close()
    # TODO: strange,need check on acc without phone number
    number_is_exists = soup.find(class_="phone_header_description").find(class_="account_data_field")
    if number_is_exists is not None:
        acc.phone_number = True


    headers["Host"] = "steamcommunity.com"
    headers["Refer"] = "https://steamcommunity.com/profiles/deadbutnotcry/friends/"
    resp = requests.get(f"https://steamcommunity.com/profiles/{id}/friends/",headers=headers)
    soup = BeautifulSoup(resp.content,"html.parser")   
    friends = soup.find(class_="friends_count")
    if friends is None:
        acc.friends_count = 0
        return acc;

    #TODO: Chat check
    return acc
