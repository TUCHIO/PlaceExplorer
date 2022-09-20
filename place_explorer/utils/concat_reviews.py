import json
import os
import glob

import pandas as pd

keys = [
    #"query",
    "name",
    "full_address",
    #"borough",
    #"street",
    #"city",
    "postal_code",
    #"country_code",
    "country",
    #"us_state",
    #"state",
    #"plus_code",
    "latitude",
    "longitude",
    #"time_zone",
    #"popular_times",
    # "site",
    # "phone",
    "type",
    # "logo",
    # "description",
    # "located_in",
    # "located_google_id",
    "category",
    "subtypes",
    "posts",
    # "reviews_tags",
    "rating",
    "reviews",
    #"reviews_data",
    "photos_count",
    #"google_id",
    #"cid",
    "place_id",
    #"reviews_link",
    #"reviews_id",
    "photo",
    "street_view",
    # "working_hours_old_format",
    # "working_hours",
    # "other_hours",
    # "business_status",
    # "about",
    # "range",
    # "reviews_per_score",
    # "reservation_links",
    # "booking_appointment_link",
    # "menu_link",
    # "order_links",
    # "owner_id",
    # "verified",
    # "owner_title",
    # "owner_link",
    # "location_link",
]

def concat_reviews(directory_path):
    jsons = glob.glob(os.path.join(directory_path, "*.json"))
    dfs = []
    for file in jsons:
        with open(file, "rt") as f:
            info = json.load(f)
        df = pd.DataFrame.from_dict(info[0]["reviews_data"])
        for key in keys:
            if key in info[0].keys():
                df[key] = info[0][key]
        dfs.append(df)
    return pd.concat(dfs, axis=0)

