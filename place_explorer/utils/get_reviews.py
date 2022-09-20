import json
import os

import pandas as pd
from tqdm import tqdm

def get_reviews(
    outscraper_client, places_csv, result_directory, reviews_limit, language="ja", save_responses=True
):
    df_places = pd.read_csv(places_csv, index_col=0)
    os.makedirs(result_directory, exist_ok=True)

    for place_id in tqdm(df_places["place_id"]):
        try:
            csv_path = os.path.join(result_directory, f"{place_id}.csv")
            if os.path.isfile(csv_path):
                continue
            url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            responses = outscraper_client.google_maps_reviews(
                url, sort="newest", language=language, reviewsLimit=reviews_limit,
            )
            if save_responses:
                with open(os.path.join(result_directory, f"{place_id}.json"), 'wt') as f:
                    json.dump(responses, f, indent=4)
        

            reviews_data = responses[0]["reviews_data"]
            df_reviews = pd.DataFrame.from_dict(reviews_data)
            df_reviews.to_csv(csv_path)
        
        except IndexError:
            print('list index out of range')
            print(place_id)
            continue
                      