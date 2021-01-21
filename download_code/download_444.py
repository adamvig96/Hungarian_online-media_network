import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle5 as pickle
import time
from datetime import datetime as dt


def get_soups(df, sleep_time=3):
    soups = []
    for index, page_link in tqdm(enumerate(list(df["url"]))):
        resp = requests.get(page_link)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            df.loc[index, "soup"] = str(soup)
        else:
            print(resp.status_code)
            df.loc[index, "soup"] = str(resp.status_code)

        time.sleep(sleep_time)

    return df


df = pd.read_pickle("data/444_all_links.pkl.pkl")

months = df["month"].unique().tolist()

df["soup"] = None


for month in months:
    # df_month = df.loc[df["month"] == month, :].reset_index(drop=True).copy()
    df_month = df.head()
    print(df_month.shape[0])
    df_month_soups = get_soups(df_month)

    df_month_soups.to_pickle("data/444/month_{month}_soups.pkl".format(month=month))
