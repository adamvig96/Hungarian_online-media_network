import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle5 as pickle
import time
from datetime import datetime as dt
import os

def get_soups(df, sleep_time=1):
    soups = []
    for index, page_link in tqdm(enumerate(list(df["link"]))):
        resp = requests.get(page_link)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            df.loc[index, "soup"] = str(soup)
        else:
            print(resp.status_code)
            df.loc[index, "soup"] = str(resp.status_code)

        time.sleep(sleep_time)

    return df



df = pd.read_csv("data/links/888_missed.csv")

df_soup = get_soups(df)

df_soup.to_pickle("data/888/888_missed_soups.pkl")


#df = pd.read_csv("data/links/888_all_links.csv")
#
#felosztas = df["felosztas"].unique().tolist()
#megvan = os.listdir("data/888")
#
#if ".ipynb_checkpoints" in megvan:
#    megvan.remove(".ipynb_checkpoints")
#
#megvan = [int(string[4:6]) for string in megvan]
#print(megvan)
#
#
#felosztas = [file for file in felosztas if file not in megvan]
#print (felosztas)
#
#df["soup"] = None
#
#
#for szam in felosztas:
#    print(szam)
#    df_month = df.loc[df["felosztas"] == szam, :].reset_index(drop=True).copy()
#    #df_month = df.head().copy()
#    print(df_month.shape[0])
#    df_month_soups = get_soups(df_month)
#
#    df_month_soups.to_pickle("data/888/888_{szam}_soups.pkl".format(szam=szam))
#