import datetime
import json
import os
import dotenv
import string
import requests
import subprocess
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


dotenv.load_dotenv()  # ez mi?

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


def get_soups(page_links, sleep_time=12):
    soups = []
    for page_link in page_links:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        soups.append(soup)
        time.sleep(sleep_time)
    return soups


# Mandiner
try:
    home = "mandiner.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day in item.get("href"):
                l.append(item.get("href"))
    links = list(set(l))

    mandiner_links = []
    for link in links:
        if "https://" not in link:
            if "#comments" not in link:
                mandiner_links.append("https://mandiner.hu" + link)

    soups = get_soups(mandiner_links)

    mandiner_out = pd.DataFrame(
        list(zip(mandiner_links, soups)), columns=["Link", "Soup"]
    )
    mandiner_out["Page"] = "Mandiner"

    print("Got Mandiner")
except:
    print("Mandiner failed")

# 444
try:
    home = "444.hu"
    day = date.today().strftime("%Y/%m/%d/")
    negy_links = get_links(home, day)
    soups = get_soups(negy_links)

    negy_out = pd.DataFrame(list(zip(negy_links, soups)), columns=["Link", "Soup"])
    negy_out["Page"] = "444"

    print("Got 444")
except:
    print("444 failed")

# HVg
try:
    home = "hvg.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day in item.get("href"):
                l.append(item.get("href"))
    links = list(set(l))

    hvg_links = []
    for link in links:
        if "https://" not in link:
            if "/360/" not in link:
                hvg_links.append("https://hvg.hu" + link)

    soups = get_soups(hvg_links)

    hvg_out = pd.DataFrame(list(zip(hvg_links, soups)), columns=["Link", "Soup"])
    hvg_out["Page"] = "HVG"

    print("Got hvg")
except:
    print("hvg failed")

# Origo
try:
    home = "www.origo.hu/index.html"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home, allow_redirects=False)
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day in item.get("href"):
                if "origo.hu" in item.get("href"):
                    l.append(item.get("href"))
    origo_links = list(set(l))

    soups = get_soups(origo_links)

    origo_out = pd.DataFrame(list(zip(origo_links, soups)), columns=["Link", "Soup"])
    origo_out["Page"] = "Origo"

    print("Got origo")
except:
    print("origo failed")

# 24.hu
try:
    home = "24.hu"
    day = date.today().strftime("%Y/%m/%d/")
    # day = "2020/06/17"
    links = get_links(home, day)

    huszon_links = []
    for link in links:
        if "https://24.hu/" in link:
            huszon_links.append(link)

    soups = get_soups(huszon_links)

    huszon_out = pd.DataFrame(list(zip(huszon_links, soups)), columns=["Link", "Soup"])
    huszon_out["Page"] = "24.hu"

    print("Got 24")
except:
    print("24 failed")

# Ripost
try:
    page = requests.get("https://ripost.hu/")
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if "ripost.hu" in item.get("href"):
                l.append(item.get("href"))
    links = list(set(l))
    ripost_links = []
    for link in links:
        if link[-8:-1].isdigit():
            ripost_links.append(link)

    soups = get_soups(ripost_links)

    ripost_out = pd.DataFrame(list(zip(ripost_links, soups)), columns=["Link", "Soup"])
    ripost_out["Page"] = "Ripost"

    print("Got ripost")
except:
    print("ripost failed")

# 888.hu
try:
    page = requests.get("https://888.hu/")
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if "888.hu" in item.get("href"):
                l.append(item.get("href"))

    links = list(set(l))
    nyolc_links = []
    for link in links:
        if link[-8:-1].isdigit():
            nyolc_links.append(link)

    soups = get_soups(nyolc_links)

    nyolc_out = pd.DataFrame(list(zip(nyolc_links, soups)), columns=["Link", "Soup"])
    nyolc_out["Page"] = "888"

    print("Got 888")
except:
    print("888 failed")

# VG
try:
    page = requests.get("https://vg.hu/")
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if "vg.hu" in item.get("href"):
                l.append(item.get("href"))
    links = list(set(l))
    vg_links = []
    for link in links:
        if link[-8:-1].isdigit():
            vg_links.append(link)

    soups = get_soups(vg_links)

    vg_out = pd.DataFrame(list(zip(vg_links, soups)), columns=["Link", "Soup"])
    vg_out["Page"] = "Világgazdaság"

    print("Got VG")
except:
    ("VG failed")

# Figyelő
try:
    page = requests.get("https://figyelo.hu/")
    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if "figyelo.hu" in item.get("href"):
                if "hetilap" not in item.get("href"):
                    l.append(item.get("href"))
    links = list(set(l))

    figyelo_links = []
    for link in links:
        if link[-7:-1].isdigit():
            figyelo_links.append(link)

    soups = get_soups(figyelo_links)

    figyelo_out = pd.DataFrame(
        list(zip(figyelo_links, soups)), columns=["Link", "Soup"]
    )
    figyelo_out["Page"] = "Figyelő"

    print("Got figyelo")
except:
    print("figyelo failed")

# Alfahír
try:
    page = requests.get("https://alfahir.hu/")
    soup = BeautifulSoup(page.content, "html.parser")

    day = date.today().strftime("%Y/%m/%d/")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day in item.get("href"):
                l.append(item.get("href"))
    links = list(set(l))

    alfahir_links = []
    for link in links:
        if "https://" not in link:
            alfahir_links.append("https://alfahir.hu" + link)

    soups = get_soups(alfahir_links)

    alfahir_out = pd.DataFrame(
        list(zip(alfahir_links, soups)), columns=["Link", "Soup"]
    )
    alfahir_out["Page"] = "Alfahír"

    print("Got alfahir")
except:
    print("alfahir failed")

# Napi.hu
try:
    page = requests.get("https://napi.hu/")
    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if "napi.hu" in item.get("href"):
                if "www.facebook.com" not in item.get("href"):
                    l.append(item.get("href"))
    links = list(set(l))

    napi_links = []
    for link in links:
        if link[-11:-5].isdigit():
            napi_links.append(link)

    soups = get_soups(napi_links)

    napi_out = pd.DataFrame(list(zip(napi_links, soups)), columns=["Link", "Soup"])
    napi_out["Page"] = "Napi.hu"

    print("Got napi")
except:
    print("napi failed")

# Index
try:
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

    print("Got index")
except:
    print("index failed")

# Nepszava
try:
    home = "nepszava.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    nepszava_links = []
    for link in links:
        if link[1:8].isdigit():
            nepszava_links.append("https://" + home + "/" + link)

    soups = get_soups(nepszava_links)

    nepszava_out = pd.DataFrame(
        list(zip(nepszava_links, soups)), columns=["Link", "Soup"]
    )
    nepszava_out["Page"] = "Népszava"
except:
    print("nepszava failed")

# pestisracok
try:
    home = "pestisracok.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    pestisracok_links = []
    for link in links:
        if "https://pestisracok.hu/" in link and "#" not in link:
            if link.count("/") == 4:
                pestisracok_links.append(link)

    soups = []
    favicon = "https://pestisracok.hu/wp-content/uploads/2015/10/favicon-16x16.gif"
    for page_link in pestisracok_links:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            if soup.find_all("meta")[1].find("link").get("href") == favicon:
                soups.append(soup)
            else:
                pestisracok_links.remove(page_link)
        except:
            pestisracok_links.remove(page_link)
        time.sleep(12)

    pestisracok_out = pd.DataFrame(
        list(zip(pestisracok_links, soups)), columns=["Link", "Soup"]
    )
    pestisracok_out["Page"] = "Pesti Srácok"
except:
    print("PSrácok failed")

# femina
try:
    home = "femina.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    femina_links = []
    for link in links:
        if "https://femina.hu/" in link:
            if link.count("/") == 5:
                femina_links.append(link)

    soups = get_soups(femina_links)

    femina_out = pd.DataFrame(list(zip(femina_links, soups)), columns=["Link", "Soup"])
    femina_out["Page"] = "Femina"
except:
    print("femina failed")

# life.hu
try:
    home = "life.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    life_links = []
    for link in links:
        if "https://www.life.hu/" in link:
            if link.split("/")[-1].split("-")[0].isdigit():
                life_links.append(link)

    soups = get_soups(life_links)

    life_out = pd.DataFrame(list(zip(life_links, soups)), columns=["Link", "Soup"])
    life_out["Page"] = "Life.hu"
except:
    print("life.hu failed")

# cosmopolitan
try:
    home = "cosmopolitan.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    cosmo_links = []
    for link in links:
        if "https://cosmopolitan.hu/" in link and link.split("/")[-3].isdigit():
            cosmo_links.append(link)

    soups = get_soups(cosmo_links)

    cosmo_out = pd.DataFrame(list(zip(cosmo_links, soups)), columns=["Link", "Soup"])
    cosmo_out["Page"] = "Cosmopolitan"
except:
    print("Cosmopolitan failed")

# nlc
try:
    home = "nlc.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    nlc_links = []
    for link in links:
        if "https://nlc.hu/" in link and link.split("/")[-3].isdigit():
            nlc_links.append(link)

    soups = get_soups(nlc_links)

    nlc_out = pd.DataFrame(list(zip(nlc_links, soups)), columns=["Link", "Soup"])
    nlc_out["Page"] = "nlc.hu"
except:
    print("nlc failed")

try:
    home = "atv.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    atv_links = []
    for link in links:
        if link.split("/")[-1].split("-")[0].isdigit():
            atv_links.append("http://www.atv.hu/" + link)

    soups = get_soups(atv_links)

    atv_out = pd.DataFrame(list(zip(atv_links, soups)), columns=["Link", "Soup"])
    atv_out["Page"] = "atv.hu"
except:
    print("atv failed")

try:
    home = "168ora.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    ora_links = []

    for link in links:
        if link.split("-")[-1].isdigit():
            ora_links.append("https://168ora.hu" + link)

    soups = get_soups(ora_links)

    ora_out = pd.DataFrame(list(zip(ora_links, soups)), columns=["Link", "Soup"])
    ora_out["Page"] = "168óra"
except:
    print("168ora failed")


try:
    home = "qubit.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    qubit_links = []
    for link in links:
        if link.split("/")[-2].isdigit():
            qubit_links.append(link)

    soups = get_soups(qubit_links)

    qubit_out = pd.DataFrame(list(zip(qubit_links, soups)), columns=["Link", "Soup"])
    qubit_out["Page"] = "Qubit"
except:
    print("qubit failed")


try:
    home = "G7.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    g7_links = []

    for link in links:
        if "https://g7.hu/" in link:
            if link.split("/")[-3].isdigit():
                g7_links.append(link)

    soups = get_soups(g7_links)

    g7_out = pd.DataFrame(list(zip(g7_links, soups)), columns=["Link", "Soup"])
    g7_out["Page"] = "G7"
except:
    print("g7 failed")

try:
    home = "portfolio.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    portfolio_links = []

    for link in links:
        if link.split("-")[-1].isdigit():
            portfolio_links.append(link)

    for i, link in enumerate(portfolio_links):
        if "https://www.portfolio.hu/" not in link:
            portfolio_links[i] = "https://www.portfolio.hu" + link

    soups = get_soups(portfolio_links)

    portfolio_out = pd.DataFrame(
        list(zip(portfolio_links, soups)), columns=["Link", "Soup"]
    )
    portfolio_out["Page"] = "Portfolio"

except:
    print("portfolio failed")


try:
    home = "direkt36.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    direkt36_links = []

    for link in links:
        if "https://www.direkt36.hu/" in link:
            if link.count("/") == 4 and "#" not in link and link.count("-") > 3:
                direkt36_links.append(link)

    soups = get_soups(direkt36_links)

    direkt36_out = pd.DataFrame(
        list(zip(direkt36_links, soups)), columns=["Link", "Soup"]
    )
    direkt36_out["Page"] = "direkt36"
except:
    print("direkt36 failed")

try:
    home = "kisalfold.hu"
    day = date.today().strftime("%Y%m%d")

    page = requests.get("https://" + home + "/")

    soup = BeautifulSoup(page.content, "html.parser")

    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            l.append(item.get("href"))
    links = list(set(l))

    kisalfold_links = []

    for link in links:
        if "https://www.kisalfold.hu/" in link:
            if link.split("/")[-2].split("-")[-1].isdigit():
                kisalfold_links.append(link)

    soups = get_soups(kisalfold_links)

    kisalfold_out = pd.DataFrame(
        list(zip(kisalfold_links, soups)), columns=["Link", "Soup"]
    )
    kisalfold_out["Page"] = "kisalfold.hu"

except:
    print("kisalfold failed")


new_posts = pd.concat(
    [
        negy_out,
        hvg_out,
        origo_out,
        huszon_out,
        ripost_out,
        nyolc_out,
        mandiner_out,
        figyelo_out,
        vg_out,
        napi_out,
        alfahir_out,
        index_out,
        nepszava_out,
        pestisracok_out,
        femina_out,
        cosmo_out,
        life_out,
        nlc_out,
        atv_out,
        kisalfold_out,
        qubit_out,
        g7_out,
        direkt36_out,
        portfolio_out,
        ora_out,
    ]
)
new_posts["Date"] = date.today()

new_posts["Soup"] = new_posts["Soup"].apply(str)

data_file_path = "links_soups_{}.pkl".format(date.today().strftime("%d-%m-%Y"))

new_posts.to_pickle(data_file_path)
print("wrote file to local")


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
