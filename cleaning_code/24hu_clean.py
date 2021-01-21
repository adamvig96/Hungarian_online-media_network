#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

data_dir = "/Users/vigadam/Documents/github/media_network/media_data/html_pages/24_hu"


# In[87]:


class _24hu:
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

            # Title
            try:
                df.loc[self.soups.index[i], "Title"] = (
                    soup.find(attrs={"itemprop": "headline"}).get_text().strip()
                )
            except:
                df.loc[self.soups.index[i], "Title"] = None

            # Text
            try:
                textlist = [
                    soup.find(attrs={"data-ce-measure-widget": "Cikk lead"})
                ] + soup.find(
                    attrs={"class": "o-post__body o-postCnt post-body"}
                ).find_all(
                    "p"
                )
                df.loc[self.soups.index[i], "Text"] = (
                    " ".join(
                        [item.get_text().strip() for item in textlist if item != None]
                    )
                    .replace("\xa0", "")
                    .strip()
                )
            except:
                df.loc[self.soups.index[i], "Text"] = None

            # Author
            try:
                df.loc[self.soups.index[i], "Author"] = soup.find(
                    attrs={"class": "m-author__name"}
                ).get_text()
            except:
                df.loc[self.soups.index[i], "Author"] = None

            # tags
            try:
                taglist = soup.find_all(
                    attrs={
                        "class": "m-tag__links a-tag -articlePageMainTags swiper-slide"
                    }
                )

                df.loc[self.soups.index[i], "Tags"] = str(
                    [item.get_text().strip().lower() for item in taglist]
                )
            except:
                df.loc[self.soups.index[i], "Tags"] = None


# In[102]:


data_files = os.listdir(data_dir + "/2020")

data_files = sorted([data_dir + "/2020/" + item for item in data_files])


# In[104]:


df_clean = pd.DataFrame()
for data_month in tqdm(data_files):

    df = pd.read_pickle(data_month)
    df["page"] = "24.hu"

    _24hu(df).clean()

    df_clean = pd.concat(
        [df_clean, df.drop(columns=["Unnamed: 0", "soup", "felosztas"])]
    )


# In[106]:


df_clean.to_csv(
    "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/media_data/clean_text/2020/24hu_clean.csv"
)


# In[ ]:
