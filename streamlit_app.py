import streamlit as st
import pandas as pd
import numpy as np
import random
import ast
from PIL import Image

with open('./style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Anime Recommendation Engine - Streamlit (ARES)")

DATA_URL = "./datafile/animes.csv"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    del data["uid"]
    del data["members"]
    return data


data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

show_nsfw = st.checkbox("Include NSFW")


if st.button("Recommend"):
    def get_random_anime():
        no_of_rows = len(data)
        random_integer = random.randint(0, no_of_rows)
        row = data.loc[random_integer]
        genre_list = ast.literal_eval(row['genre'])
        if ("Hentai" in genre_list or "Ecchi" in genre_list) and not show_nsfw:
            get_random_anime()
        else:
            for i in range(len(row)):
                if row.index[i] == "img_url":
                    st.image(row.iloc[i], caption=row["title"], use_column_width=False)
                if row.index[i] == "link":
                    st.write("{} : {}".format(str(row.index[i]).capitalize(), row.iloc[i]))

            st.table(row.drop('img_url').drop('link'))
    
    get_random_anime()



