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

data_dir = "/Users/vigadam/Documents/github/media_network/media_data/html/mno/"


# In[64]:


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

    def clean(self):
        self.title()
        self.link()
        self.author()
        self.text_date_tags_source()
        # self.source()
        # self.tags()


# In[65]:


class Mno(Helper):
    def __init__(self, df):
        self.data = df
        self.soups = self.data["soup"].dropna()

    def title(self):
        Helper.title_main(self, "class", "et_main_title")

    def text_date_tags_source(self):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                textlist = (
                    BeautifulSoup(soup)
                    .find(attrs={"class": "entry-content clearfix"})
                    .find_all("p")
                )

                df.loc[self.soups.index[i], "Text"] = (
                    " ".join([item.get_text().strip() for item in textlist])
                    .replace("\xa0", "")
                    .strip()
                )
                date_text = (
                    BeautifulSoup(soup)
                    .find(attrs={"class": "en-article-dates-main"})
                    .get_text()
                    .split(" ")
                )

                df.loc[self.soups.index[i], "year"] = date_text[0].replace(".", "")
                df.loc[self.soups.index[i], "month"] = date_text[1]
                df.loc[self.soups.index[i], "day"] = date_text[2].replace(".", "")

            except AttributeError:
                df.loc[self.soups.index[i], "Text"] = None
                df.loc[self.soups.index[i], "year"] = None
                df.loc[self.soups.index[i], "month"] = None
                df.loc[self.soups.index[i], "day"] = None
            try:
                df.loc[self.soups.index[i], "Tags"] = str(
                    [
                        item.get_text()
                        for item in BeautifulSoup(soup)
                        .find(attrs={"class": "en-article-tags"})
                        .find_all("a")
                    ]
                )

            except:
                df.loc[self.soups.index[i], "Tags"] = None

            try:
                df.loc[self.soups.index[i], "Source"] = (
                    BeautifulSoup(soup)
                    .find(attrs={"class": "en-article-source col-sm"})
                    .get_text()
                    .strip()
                )

            except:
                df.loc[self.soups.index[i], "Source"] = None

    def author(self):
        Helper.author_main(self, "class", "en-article-author")

    def source(self):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Source"] = (
                    BeautifulSoup(soup)
                    .find(attrs={"class": "en-article-source col-sm"})
                    .get_text()
                    .strip()
                )

            except:
                df.loc[self.soups.index[i], "Source"] = None

    def tags(self):
        for i, soup in tqdm(enumerate(self.soups)):
            try:
                df.loc[self.soups.index[i], "Tags"] = str(
                    [
                        item.get_text()
                        for item in BeautifulSoup(soup)
                        .find(attrs={"class": "en-article-tags"})
                        .find_all("a")
                    ]
                )

            except:
                df.loc[self.soups.index[i], "Tags"] = None


# In[66]:


data_files = os.listdir(data_dir + "/2020")

data_files = [data_dir + "/2020/" + item for item in data_files]


# In[67]:


df_clean = pd.DataFrame()
for data_file in tqdm(data_files):

    df = pd.read_pickle(data_file)

    Mno(df).clean()

    df_clean = pd.concat([df_clean, df.drop(columns=["Unnamed: 0", "soup"])])


df_clean = df_clean.reset_index(drop=True)


df_clean.to_pickle(
    "/Users/vigadam/Documents/github/media_network/media_data/clean/pickle/2020/"
    + "mno_clean.pkl"
)
