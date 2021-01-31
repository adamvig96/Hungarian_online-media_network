import pandas as pd
import numpy as np
import os
import re

# importing required modules
from tqdm import tqdm
from pdfminer import high_level


dir = "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/speech_text/"


def clean_text(df):
    try:
        try:
            stopwords = [
                df.loc[0, 0]
                .split("Az ülésen jelen voltak:")[1]
                .split("\n\n")[-4]
                .strip(),
                "-\n",
                "\n",
                "\x0c",
            ]
        except IndexError:
            stopwords = [
                df.loc[0, 0]
                .split("Az ülésen jelen volt:")[1]
                .split("\n\n")[-4]
                .strip(),
                "-\n",
                "\n",
                "\x0c",
            ]

        regex = re.compile(".*?\((.*?)\)")

        hun_letters = {
            "Á": "A",
            "É": "E",
            "Ő": "O",
            "Ö": "O",
            "Ó": "O",
            "Ü": "U",
            "Ú": "U",
            "Ű": "U",
        }

        df["name_list"] = None
        df["date"] = stopwords[0]

        for i in range(df.shape[0]):

            # basic cleaner
            for stopword in stopwords:
                df.loc[i, 0] = df.loc[i, 0].replace(stopword, "").strip()

            # delete comments
            result = re.findall(regex, df.loc[i, 0])
            result.append("()")

            for res in result:
                df.loc[i, 0] = df.loc[i, 0].replace(res, "").strip()

            # hungarian ÁÉÖŐÓÜÚŰ to AEOU
            for letter in hun_letters.keys():
                df.loc[i, 0] = df.loc[i, 0].replace(letter, hun_letters[letter])

            # extract name list
            df.loc[i, "name_list"] = [
                item.strip()
                for item in re.findall("[A-Z\s]+", df.loc[i, 0])
                if len(item.strip()) > 6
            ]

        df = (
            df.loc[df["name_list"].apply(len) != 0].iloc[1:-1, :].reset_index(drop=True)
        )

        df["name"] = df["name_list"].apply(lambda x: x[0])

        df["text"] = df.apply(lambda x: x[0].split(x["name"])[-1].strip(), axis=1)

        for i in range(df.shape[0]):
            if df.loc[i, "text"][0] == ":":
                df.loc[i, "text"] = df.loc[i, "text"][1:].strip()
            else:
                df.loc[i, "text"] = " ".join(df.loc[i, "text"].split(":")[1:])

        df["len"] = df["text"].apply(len)
        df = df.rename(columns={0: "raw"})

    except:
        print(file)
        pass

    return df


file_list = [dir + "naplok/" + string for string in os.listdir(dir + "naplok/")]

if dir + "naplok/.DS_Store" in file_list:
    file_list.remove(dir + "naplok/.DS_Store")


file_list.remove(dir + "naplok/ny200502-unnepiules.pdf")


df_concated = pd.DataFrame()
for file in tqdm(file_list):
    string = high_level.extract_text(file)
    df = pd.DataFrame(string.split("ELNÖK: "))
    df = clean_text(df)

    df_concated = pd.concat([df_concated, df])


df_concated.to_pickle("text_speeches.pkl")
