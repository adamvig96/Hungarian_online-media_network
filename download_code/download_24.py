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


df = pd.read_csv("data/links/24_2020_links.csv")


felosztas = df["felosztas"].unique().tolist()
megvan = os.listdir("data/24")

if ".ipynb_checkpoints" in megvan:
    megvan.remove(".ipynb_checkpoints")

megvan = [int(string[5:7]) for string in megvan]
print(megvan)


felosztas = [file for file in felosztas if file not in megvan]
print (felosztas)


df["soup"] = None


for num in felosztas:
    df_num = df.loc[df["felosztas"] == num, :].reset_index(drop=True).copy()
    #df_num = df.head(100).copy()
    print(df_num.shape[0])
    df_num_soups = get_soups(df_num)

    df_num_soups.to_pickle("data/24/2020_{num}_soups.pkl".format(num=num))
