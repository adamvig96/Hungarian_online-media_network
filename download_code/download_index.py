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
    for index, page_link in enumerate(list(df["url"])):
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        df.loc[index, "soup"] = str(soup)
        time.sleep(sleep_time)

    return df


df = pd.read_pickle("data/index_url.pkl")


for month in months:
    df_month = df.loc[df["month"] == month, :].reset_index(drop=True).copy()
    print(df_month.shape[0])
    df_month_soups = get_soups(df_month)

    df_month_soups.to_pickle("data/index/month_{month}_soups.pkl".format(month=month))
