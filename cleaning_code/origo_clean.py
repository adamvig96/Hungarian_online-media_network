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
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import warnings
data_dir = "/Users/vigadam/Documents/github/media_network/data/origo/"


# In[91]:


class Helper:
    import json

    from bs4 import BeautifulSoup
    import bs4

    import pandas as pd
    import numpy as np

    import re

    import warnings

    warnings.filterwarnings("ignore")

    def __init__(self, df):
        None

    def title_main(self, element, id_):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Title"] = (
                    BeautifulSoup(soup).find(attrs={element: id_}).get_text()
                )
            except AttributeError:
                df.loc[self.soups.index[i], "Title"] = None

    def link(self):
        for i, soup in tqdm(enumerate(self.soups)):
            soup_for_links = BeautifulSoup(soup).find_all("a")
            link_list = []
            for item in soup_for_links:
                if type(item.get("href")) == str:
                    link_list.append(item.get("href"))
            df.loc[self.soups.index[i], "links"] = str(list(set(link_list)))

    def text_main(self, element, class_id):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                soup_for_text = (
                    BeautifulSoup(soup)
                    .find(element, class_=re.compile(class_id))
                    .find_all("p")
                )
                text_list = []
                for item in soup_for_text:
                    if soup_for_text != "":
                        text_list.append(item.text)
                df.loc[self.soups.index[i], "Text"] = " ".join(text_list)
            except AttributeError:
                df.loc[self.soups.index[i], "Text"] = None

    def author_main(self, element, class_id):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Author"] = (
                    BeautifulSoup(soup)
                    .find(attrs={element:class_id})
                    .get_text()
                    .strip()
                )
            except:
                df.loc[self.soups.index[i], "Author"] = None

    def category_main(self, element, id_):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Category"] = (
                    BeautifulSoup(soup).find(attrs={element: id_}).text.strip()
                )

            except:
                df.loc[self.soups.index[i], "Category"] = None

    def tags_main(self, element, id_):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Tags"] = (
                    BeautifulSoup(soup)
                    .find(attrs={element: id_}).text.strip()
                )

            except:
                df.loc[self.soups.index[i], "Tags"] = None
        df["Tags"] = df["Tags"].str.split("\n\n\n")

    def clean(self):
        self.title()
        self.text()
        self.link()
        self.author()
        self.tags()


# In[130]:


class Origo(Helper):
    def __init__(self, df):
        page = "origo"
        self.data = df.loc[df["page"] == page]
        self.soups = self.data["soup"].dropna()

    def title(self):
        Helper.title_main(self, "class", "article-title")

    def text(self):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                textlist = BeautifulSoup(soup).find(
                    attrs={"class": "article-lead"}
                ).find_all("p") + BeautifulSoup(soup).find(
                    attrs={"class": "article-content"}
                ).find_all(
                    "p"
                )

                df.loc[self.soups.index[i], "Text"] = (
                    " ".join([item.get_text().strip() for item in textlist])
                    .replace("\xa0", "")
                    .strip()
                )
            except AttributeError:
                df.loc[self.soups.index[i], "Text"] = None

    def author(self):
        Helper.author_main(self, "class", "article-author")

    def tags(self):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Tags"] = str([
                    item.get("title")
                    for item in BeautifulSoup(soup)
                    .find_all(attrs={"class": "article-meta"})[0]
                    .find_all("a")[1:]
                ])

            except:
                df.loc[self.soups.index[i], "Tags"] = None


# In[83]:


data_list = sorted([
    "month_04_soups.pkl",
    "month_12_soups.pkl",
    "month_03_soups.pkl",
    "month_06_soups.pkl",
    "month_07_soups.pkl",
    "month_02_soups.pkl",
    "month_10_soups.pkl",
    "month_08_soups.pkl",
    "month_05_soups.pkl",
    "month_11_soups.pkl",
    "month_01_soups.pkl",
    "month_09_soups.pkl",
])

data_files = [data_dir + item for item in data_list]


# In[141]:


df_clean = pd.DataFrame()
for data_month in tqdm(data_files):

    df = pd.read_pickle(data_month)
    df["page"] = "origo"

    Origo(df).clean()

    df_clean = pd.concat([df_clean, df.drop(columns=["Unnamed: 0", "soup"])])


# In[109]:


df_clean.to_pickle(data_dir + "origo_clean.pkl")


# In[ ]:




