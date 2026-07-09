from serpapi import GoogleSearch
import os
import time
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from utils import clean_number
from utils import clean_url

load_dotenv()


def scrape_businesses(api_key, query, coords, max_results=100):
    all_results = []

    start = 0

    while start < max_results:

        params = {
            "engine": "google_maps",
            "q": query,
            "ll": coords,
            "hl": "en",
            "gl": "za",
            "start": start,
            "api_key": api_key,
        }

        search = GoogleSearch(params)
        result = search.get_dict()

        local_results = result.get("local_results", [])

        if not local_results:
            break

        all_results.extend(local_results)

        pagination = result.get("serpapi_pagination", {})

        if "next" not in pagination:
            break

        start += 20

        time.sleep(0.2)

    details = []

    for place in all_results:

        details.append(
            [
                place.get("title"),
                place.get("rating"),
                place.get("reviews"),
                clean_number(place.get("phone")),
                clean_url(place.get("website")),
            ]
        )

    df = pd.DataFrame(
        details,
        columns=["Title", "Rating", "Reviews", "Phone", "Website"]
    )

    df = df[df["Phone"].notna()]
    df = df.drop_duplicates()
    df = df.dropna(subset=["Title", "Phone"])

    return df


def save_report(df, query):

    now = datetime.now()

    filename = f"lead_data_{query}_{now.strftime('%Y-%m-%d_%H-%M')}.csv"

    os.makedirs("reports", exist_ok=True)

    path = os.path.join("reports", filename)

    df.to_csv(path, index=False)

    return path


if __name__ == "__main__":

    api_key = os.getenv("SERPAPI_KEY")

    query = input("Search Query: ")

    location = input("Location: ")

    results = scrape_businesses(
        api_key,
        query,
        location,
        100
    )

    file = save_report(results, query)

    print(f"Saved {len(results)} businesses")
    print(file)