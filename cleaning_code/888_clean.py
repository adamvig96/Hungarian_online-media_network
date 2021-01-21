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

data_dir = "/Users/vigadam/Documents/github/media_network/media_data/html_pages/888"


# In[186]:


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

    def title_main(self, element, _id):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Title"] = (
                    BeautifulSoup(soup).find(attrs={element: _id}).get_text().strip()
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

    def author_main(self, element, _id):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Author"] = (
                    BeautifulSoup(soup).find(attrs={element: _id}).get_text().strip()
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
                    BeautifulSoup(soup).find(attrs={element: id_}).text.strip()
                )

            except:
                df.loc[self.soups.index[i], "Tags"] = None
        df["Tags"] = df["Tags"].str.split("\n\n\n")

    def clean_(self):
        self.title()
        self.text()
        self.link()
        self.author()
        self.source()
        self.tags()


class _888(Helper):
    def __init__(self, df):
        self.data = df
        self.soups = self.data["soup"].dropna()

    def clean(self):
        for i, Soup in tqdm(enumerate(self.soups)):

            soup = BeautifulSoup(Soup)

            # Title
            try:
                df.loc[self.soups.index[i], "Title"] = (
                    soup.find("h1").get_text().strip()
                )
            except:
                df.loc[self.soups.index[i], "Title"] = None

            # Text
            try:
                textlist = [soup.find(attrs={"class": "high-lite"})] + soup.find(
                    attrs={"class": "maincontent8"}
                ).find_all("p")
                df.loc[self.soups.index[i], "Text"] = (
                    " ".join([item.get_text().strip() for item in textlist])
                    .replace("\xa0", "")
                    .strip()
                )
            except:
                df.loc[self.soups.index[i], "Text"] = None

            # Author
            try:
                df.loc[self.soups.index[i], "Author"] = (
                    soup.find(attrs={"class": "note-block"}).get_text().strip()
                )
            except:
                df.loc[self.soups.index[i], "Author"] = None

            # date
            try:
                df.loc[self.soups.index[i], "date"] = (
                    soup.find(attrs={"id": "cikkholder"})
                    .find("p")
                    .get_text()
                    .split(" ")[0][:-1]
                    .replace(".", "-")
                )
            except:
                df.loc[self.soups.index[i], "date"] = None

            # tags
            try:
                taglist = soup.find(attrs={"class": "plugin-holder"}).find_all(
                    attrs={"rel": "tag"}
                )
                df.loc[self.soups.index[i], "Tags"] = str(
                    [item.get_text().strip().lower() for item in taglist]
                )
            except:
                df.loc[self.soups.index[i], "Tags"] = None


# In[199]:


data_files = os.listdir(data_dir + "/all")

data_files = [data_dir + "/all/" + item for item in data_files]


# In[249]:


df_clean = pd.DataFrame()
for data_file in tqdm(data_files):

    df = pd.read_pickle(data_file)
    df = df.loc[df["soup"] != "404"]

    _888(df).clean()

    df_clean = pd.concat([df_clean, df.drop(columns=["Unnamed: 0", "soup"])])


# In[ ]:


df_clean.to_pickle(
    "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/media_data/clean_text/pickle_format/888_clean_all.pkl"
)
