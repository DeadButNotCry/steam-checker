import os
import shutil
import sqlite3
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from Models.Account import Account
from checker.netscape_loader import str_format, json_cookies


def start_checking(state):
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    # opt = webdriver.ChromeOptions()
    # opt.add_argument(f"user-agent={user_agent}")
    # driver = webdriver.Chrome(r'chromedriver',options=opt)
    # driver.get("https://steamcommunity.com/id/idydalekosolnce")
    # driver.delete_all_cookies()
    try:
        for filename in os.listdir("cookies"):
            res = cookie_check(filename, state, None, user_agent)
            if res.works and not res.duplicate:
                shutil.copy(f"cookies/{filename}", f"result/valid/{filename}")
                if res.friends_count != 0:
                    shutil.copy(f"cookies/{filename}", f"result/friends/{filename}")
                else:
                    shutil.copy(f"cookies/{filename}", f"result/empty/{filename}")
                if not res.is_russia:
                    shutil.copy(f"cookies/{filename}", f"result/not_ru/{filename}")
                if res.phone_number:
                    shutil.copy(f"cookies/{filename}", f"result/verified/{filename}")
    finally:
        # driver.close()
        # driver.quit()
        pass


def cookie_check(file_name, state, driver, user_agent):
    f = open(f"cookies/{file_name}", "r")
    cookie = f.read()
    cookies = str_format(cookie)
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Refer": "https://steamcommunity.com/",
        "Host": "store.steampowered.com"
    }
    t1 = datetime.now()
    resp = requests.get("https://store.steampowered.com/account/", headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    steam_id = soup.find(class_="youraccount_steamid")
    acc = Account()
    if steam_id is None:
        acc.works = False
        state.INV += 1
        return acc
    id = steam_id.text.split(" ")[2]
    acc.id = id
    t2 = datetime.now()
    print((t2 - t1).total_seconds())
    # Check for duplicates
    con = sqlite3.connect("duplicate.db")
    res_from_db = con.execute('SELECT * FROM duplicates WHERE id=?', (id,))
    id_from_db = res_from_db.fetchone()
    if id_from_db is not None:
        acc.duplicate = True
        state.DUPL += 1
        con.close()
        return acc
    else:
        acc.duplicate = False
        # TODO: save new acc to db
        con.execute('INSERT INTO duplicates (id) VALUES (?)', (id,))
        con.commit()
        con.close()

    # TODO: strange,need check on acc without phone number
    number_is_exists = soup.find(class_="phone_header_description").find(class_="account_data_field")
    if number_is_exists is not None:
        acc.phone_number = True

    # Country check
    country = soup.find(class_="country_settings").find("span").text
    acc.is_russia = country == "Russian Federation"
    t3 = datetime.now()
    print((t3 - t2).total_seconds())
    # Friends Check
    link_to_acc = soup.find(class_="user_avatar").get("href")
    print(link_to_acc)
    new_headers = headers = {
        "User-Agent": user_agent,
        "Cookie": cookies,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Refer": "https://store.steampowered.com/",
        "Host": "steamcommunity.com"
    }
    new_resp = requests.get(link_to_acc, headers=new_headers)

    new_soup = BeautifulSoup(new_resp.content, "html.parser")
    acc.friends_count = len(new_soup.find_all(class_="friendBlock"))
    state.FRIENDS += acc.friends_count
    print((datetime.now() - t1).total_seconds())
    return acc
    # try:
    #
    #     cookies_sel = json_cookies(cookie)
    #     for c in cookies_sel:
    #         driver.add_cookie(c)
    #     driver.refresh()
    #     driver.find_element(by=By.XPATH, value='//*[@id="global_actions"]/a/img').click()
    #     try:
    #         el = driver.find_element(By.XPATH,
    #                                  '//*[@id="responsive_page_template_content"]/div[1]/div[2]/div/div[1]/div[4]/div[1]/a/span[2]')
    #         acc.friends_count = int(el.text)
    #         state.FRIENDS += int(el.text)
    #         print((datetime.now() - t3).total_seconds())
    #         print((datetime.now() - t1).total_seconds())
    #         driver.delete_all_cookies()
    #         return acc
    #     except NoSuchElementException:
    #         driver.delete_all_cookies()
    #         acc.friends_count = 0
    #         return acc
    # finally:
    #     pass
