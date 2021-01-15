import requests
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pickle

page_types = [
    #"https://24.hu/tech/",
    "https://24.hu/szorakozas/",
    "https://24.hu/kultura/",
    "https://24.hu/fn/uzleti-tippek/",
    "https://24.hu/fn/gazdasag/",
    "https://24.hu/kulfold/",
    "https://24.hu/kozelet/",
    "https://24.hu/belfold/",
    "https://24.hu/tudomany/",
    "https://24.hu/kistotal/",
    "https://24.hu/velemeny/",
    "https://24.hu/szorakozas/",
    "https://24.hu/otthon/",
    "https://24.hu/elet-stilus/",
    "https://24.hu/sport/"
]

max_page = 100000
for page_type in page_types:
    articles_page_type = []
    boolean = True
    print(page_type)
    while boolean:
        for page_number in tqdm(range(1, max_page)):
            page_link = page_type + f"page/{page_number}"

            try:
                response = requests.get(page_link)
            except TimeoutError or ConnectionError:
                print(page_link)
                pass

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("a", class_="m-articleWidget__linkImgWrap")
            articles_page_type = articles_page_type + [
                article.get("href") for article in articles
            ]

            if soup.find(attrs={"class": "next page-numbers"}) == None:
                boolean = False
                break
    df = pd.DataFrame(articles_long).drop_duplicates()
    df.to_pickle("data/links/24/24_{page_type}.pkl".format(page_type=page_type))
