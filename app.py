import datetime
import json
import os

import streamlit as st

from main import scrape_businesses

CONFIG_FILE = "config.json"


def load_config():

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    return {}


def save_config(data):

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


config = load_config()

if "api_key" not in st.session_state:
    st.session_state.api_key = config.get("api_key", "")

st.set_page_config(
    page_title="Business Scraper",
    layout="wide"
)

st.title("Business Scraper")

api_key = st.text_input(
    "SerpAPI Key",
    type="password",
    value=st.session_state.api_key,
)

query = st.text_input("Search Query")

coordinate = st.text_input(
    "Coordinates",
    value="@-26.1715215,28.0400245,12z"
)

max_results = st.number_input(
    "Max Results",
    min_value=20,
    max_value=500,
    step=20,
    value=100,
)

if api_key != st.session_state.api_key:
    st.session_state.api_key = api_key
    save_config({"api_key": api_key})

if st.button("Start Scrape", use_container_width=True):

    if not api_key:
        st.error("Please enter your SerpAPI key.")
        st.stop()

    if not query:
        st.error("Please enter a search query.")
        st.stop()

    if not coordinate:
        st.error("Please enter a coordinate string (latitude,longitude).")
        st.stop()

    with st.spinner("Scraping businesses..."):

        try:

            df = scrape_businesses(
                api_key,
                query,
                coordinate,
                max_results,
            )

            if df.empty:
                st.warning("No businesses found.")

            else:

                st.success(f"Found {len(df)} businesses.")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download CSV",
                    csv,
                    file_name=f"{query.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        except Exception as e:

            st.error(str(e))