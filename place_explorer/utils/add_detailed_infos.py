import time

import googlemaps
import matplotlib.pyplot as plt
import numpy as np
import outscraper
import pandas as pd
import plotly.express as px
from tqdm import tqdm

def get_info(place_id, outscraper_client):
    url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    responses = outscraper_client.google_maps_reviews(
        url,
        sort="newest",
        language="ja",
        reviewsLimit=1,
    )
    # print(responses[0])
    try:
        return {
            "place_id": place_id,
            "name": responses[0]["name"],
            "reviews": responses[0]["reviews"],
            "latitude": responses[0]["latitude"],
            "longitude": responses[0]["longitude"],
            "category": responses[0]["category"],
            "rating": responses[0]["rating"],
        }
    except KeyError:
        return {
            "place_id": place_id,
            "name": responses[0]["name"],
            "reviews": None,
            "latitude": None,
            "longitude": None,
            "category": None,
            "rating": None,
        }
    
def add_detailed_infos(csv_path, detailed_csv_path, outscraper_api_key):
    outscraper_client = outscraper.ApiClient(outscraper_api_key)
    df = pd.read_csv(csv_path)
    infos = []
    for idx, series in tqdm(df.iterrows(), total=len(df)):
        for i in range(3):
            try:
                place_id = series["place_id"]
                info = get_info(place_id, outscraper_client)
                infos.append(info)
                pd.DataFrame(infos).to_csv(detailed_csv_path)
                time.sleep(1)
                break
            except IndexError:
                if i == 2:
                    print("list index out of range")
                    print(idx)
                    print(series)
                time.sleep(10)
                continue