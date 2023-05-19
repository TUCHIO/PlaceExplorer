import os
import time

import googlemaps
import matplotlib.pyplot as plt
import numpy as np
import outscraper
import pandas as pd
import plotly.express as px
from tqdm import tqdm

def get_info(place_id, outscraper_client, language="en"):
    url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    responses = outscraper_client.google_maps_reviews(
        url,
        sort="newest",
        language=language,
        limit=1,
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
    
def add_detailed_infos(csv_path, detailed_csv_path, outscraper_api_key, language="en"):
    outscraper_client = outscraper.ApiClient(outscraper_api_key)
    df = pd.read_csv(csv_path)
    if os.path.isfile(detailed_csv_path):
        infos = pd.read_csv(detailed_csv_path).to_dict("records")
    else:
        infos = []
    place_ids_done = [info["place_id"] for info in infos]
        
    for idx, series in tqdm(df.iterrows(), total=len(df)):
        if series["place_id"] in place_ids_done:
            continue
        for i in range(3):
            try:
                place_id = series["place_id"]
                info = get_info(place_id, outscraper_client, language=language)
                infos.append(info)
                pd.DataFrame(infos).to_csv(detailed_csv_path, index=False)
                time.sleep(1)
                break
            except IndexError:
                if i == 2:
                    print("list index out of range")
                    print(idx)
                    print(series)
                time.sleep(10)
                continue
