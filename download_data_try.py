import datetime
import json
import os
import dotenv
import string
import requests
import dropbox

from bs4 import BeautifulSoup
import bs4
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import re
import arrow
import sqlalchemy


dotenv.load_dotenv()

# Alap függvények


def get_links(home_string, day_string):
    page = requests.get("https://" + home + "/", allow_redirects=False)
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day_string in item.get("href"):
                if home_string in item.get("href"):
                    l.append(item.get("href"))
    links = list(set(l))
    return links


def get_soups(page_links, sleep_time=3):
    soups = []
    for page_link in page_links:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        soups.append(soup)
        time.sleep(sleep_time)
    return soups


# Index
home = "index.hu"
day = date.today().strftime("%%2F%Y%%2F%m%%2F%d")
links = get_links(home, day)

index_links = []
for i in range(len(links)):
    if "mindekozben" not in links[i]:
        index_links.append(links[i])

soups = get_soups(index_links)

index_out = pd.DataFrame(list(zip(index_links, soups)), columns=["Link", "Soup"])
index_out["Page"] = "Index"


index_out["Date"] = date.today()

index_out["Soup"] = index_out["Soup"].apply(str)

data_file_path = "links_soups_{}.pkl".format(date.today().strftime("%d-%m-%Y"))

index_out.to_pickle(data_file_path)
print("out")

subprocess.call(
    [
        "scp",
        "-P",
        "2222",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        data_file_path,
        "rajk@146.110.60.20:/var/www/rajk/cikkek",
    ]
)
