#!/usr/bin/env python
# coding: utf-8

# In[119]:


import pickle
import json
import sys
import os
import string
import requests
import ast  # for string to list: ast.literal_eval()
from bs4 import BeautifulSoup
import bs4
import time
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import warnings

data_dir = "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/media_data/html_pages/index/2020/"


# In[120]:


class Index:
    import json

    from bs4 import BeautifulSoup
    import bs4

    import pandas as pd
    import numpy as np

    import re

    import warnings

    warnings.filterwarnings("ignore")

    def __init__(self, df):
        self.data = df
        self.soups = self.data["soup"].dropna()

    def clean(self):
        for i, Soup in tqdm(enumerate(self.soups)):

            soup = BeautifulSoup(Soup)

            # Text
            try:
                textlist = textlist = soup.find_all(attrs={"class": "cikk-torzs"})
                df.loc[self.soups.index[i], "Text"] = (
                    " ".join(
                        [item.get_text().strip() for item in textlist if item != None]
                    )
                    .replace("\xa0", "")
                    .replace("\n", " ")
                    .strip()
                )
            except:
                df.loc[self.soups.index[i], "Text"] = None

            # Author
            try:
                if type(df.loc[i, "alnevek"]) == str:
                    author = str(
                        [
                            item.get_text().strip()
                            for item in BeautifulSoup(df.loc[i, "alnevek"]).find_all(
                                "a"
                            )
                        ]
                    )
                elif df.loc[i, "rovat_slug"] == "mindekozben":
                    author = soup.find(attrs={"class": "name"}).get_text().strip()
                else:
                    author = (
                        soup.find(attrs={"class": "szerzok_container"})
                        .get_text()
                        .strip()
                    )
                df.loc[self.soups.index[i], "Author"] = author
            except:
                df.loc[self.soups.index[i], "Author"] = None

            # tags
            try:
                df.loc[self.soups.index[i], "Tags"] = str(
                    [item["name"] for item in df.loc[i, "tags"]]
                )
            except:
                df.loc[self.soups.index[i], "Tags"] = None


# In[155]:


data_files = os.listdir(data_dir)
data_files.remove(".DS_Store")
data_files = sorted([data_dir + item for item in data_files])


df_clean = pd.DataFrame()

for data_month in tqdm(data_files):

    df = pd.read_pickle(data_month)
    df["page"] = "Index"

    Index(df).clean()

    df_clean = pd.concat([df_clean, df.drop(columns=["soup"])])


# In[ ]:


df_clean.to_csv(
    "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/media_data/clean_text/2020/index_clean.csv"
)
