import os
import pickle
import time

import googlemaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px


class PlaceExplorer:
    def __init__(
        self,
        latitude,
        longitude,
        radius,
        google_api_key,
        filename,
        grid_size=1,
        overwrite=False,
    ):
        self.earth_radius = 6367e3
        self.latitude = latitude
        self.longitude = longitude
        self.filename = filename
        self.grid_size = grid_size
        xs = np.linspace(-radius, radius, int(2 * radius / grid_size + 1))
        ys = xs.copy()
        self.grid_xs, self.grid_ys = np.meshgrid(xs, ys)
        self.grid_done = np.zeros_like(self.grid_xs)
        i, j = self.get_next_indices()
        self.grid_done[i, j] = 100
        self.google_api_key = google_api_key
        self.google_client = googlemaps.Client(google_api_key)
        self.infos = []
        self.log = []
        self.save(overwrite=overwrite)

    def save(self, overwrite=True):
        if os.path.isfile(self.filename) and not overwrite:
            raise Exception(f"File already exists: {self.filename}")
        data = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "grid_size": self.grid_size,
            "grid_xs": self.grid_xs,
            "grid_ys": self.grid_ys,
            "grid_done": self.grid_done,
            "google_api_key": self.google_api_key,
            "infos": self.infos,
        }
        with open(self.filename, "wb") as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
        instance = cls(
            latitude=data["latitude"],
            longitude=data["longitude"],
            radius=1,
            google_api_key=data["google_api_key"],
            filename=filename,
            overwrite=True,
        )
        instance.grid_size = data["grid_size"]
        instance.grid_xs = data["grid_xs"]
        instance.grid_ys = data["grid_ys"]
        instance.grid_done = data["grid_done"]
        instance.infos = data["infos"]
        return instance

    def import_result(self, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
        radius = data["grid_xs"].max()
        latitude = data["latitude"]
        longitude = data["longitude"]
        dx = (
            (longitude - self.longitude)
            * self.earth_radius
            * np.cos(self.latitude)
            * np.pi
            / 180
        )
        dy = (latitude - self.latitude) * self.earth_radius * np.pi / 180
        mask = ((self.grid_xs - dx) ** 2 + (self.grid_ys - dy) ** 2) < radius**2
        self.grid_done[mask] = 100
        self.infos.extend(data["infos"])
        self.drop_duplicates()

    def __call__(self, max_radius=100000):
        latitude = self.latitude
        longitude = self.longitude
        while True:
            print("get_next_indices")
            i, j = self.get_next_indices()
            latitude, longitude = self.get_next_location()
            print(latitude, longitude)
            print("get_infos_nearby")
            radius = self.get_next_radius()
            while True:
                print(f"radius:　{radius}")
                infos = self.get_infos_nearby(latitude, longitude, radius)
                print(f"len: {len(infos)}")
                if len(infos) == 60:
                    radius *= 0.8
                elif len(infos) < 20:
                    radius /= 0.9
                else:
                    break
                if radius >= max_radius:
                    radius = max_radius
                    print(f"radius:　{radius}")
                    infos = self.get_infos_nearby(latitude, longitude, radius)
                    print(f"len: {len(infos)}")
                    break

            self.log.append({'radius':radius, 'latitude':latitude, 'longitude':longitude})
            self.infos.extend(infos)
            self.drop_duplicates()
            self.register_searched_area(i, j, radius)
            self.show_grid_done()
            self.show_centers()
            self.save()
            if np.sum(self.grid_done == 0.0) == 0:
                break

    def drop_duplicates(self):
        place_ids = [info["place_id"] for info in self.infos]
        _, indices = np.unique(place_ids, return_index=True)
        self.infos = [self.infos[i] for i in indices]

    def get_next_indices(self):
        grid_distances = np.sqrt(self.grid_xs**2 + self.grid_ys**2)
        distances = grid_distances + (self.grid_done > 0.0) * 1e30
        i, j = np.unravel_index(np.argmin(distances), distances.shape)
        return i, j

    def get_next_location(self):
        i, j = self.get_next_indices()
        x, y = self.grid_xs[i, j], self.grid_ys[i, j]
        delta_longitude = (
            np.arctan(x / (self.earth_radius * np.cos(self.latitude * np.pi / 180))) * 180 / np.pi
        )
        delta_latitude = np.arctan(y / self.earth_radius) * 180 / np.pi
        longitude = self.longitude + delta_longitude
        latitude = self.latitude + delta_latitude
        return latitude, longitude

    def get_next_radius(self):
        i, j = self.get_next_indices()
        if i == 0:
            i_min = 0
            i_max = i + 1
        elif i == self.grid_done.shape[0] - 1:
            i_min = i - 1
            i_max = i
        else:
            i_min = i - 1
            i_max = i + 1
        if j == 0:
            j_min = 0
            j_max = j + 1
        elif j == self.grid_done.shape[1] - 1:
            j_min = j - 1
            j_max = j
        else:
            j_min = j - 1
            j_max = j + 1
        local_grid = self.grid_done[i_min : i_max + 1, j_min : j_max + 1]
        return local_grid.max()

    def register_searched_area(self, i, j, radius):
        coordination = self.grid_xs[i, j], self.grid_ys[i, j]
        distances = np.sqrt(
            (self.grid_xs - coordination[0]) ** 2
            + (self.grid_ys - coordination[1]) ** 2
        )
        self.grid_done[distances < radius] = radius

    def show_grid_done(self):
        plt.contourf(self.grid_done)
        plt.show()
        plt.cla()
        plt.clf()
        plt.close()
        
    def show_centers(self):
        df = pd.DataFrame(self.log)
        fig = px.scatter_mapbox(
            df.dropna(),
            lat="latitude",
            lon="longitude",
            size="radius",
            # hover_name="name",
            # hover_data=['reviews', 'category', 'rating'],
            # color="sqrt_reviews",
            # color_continuous_scale=px.colors.sequential.Bluered,
            height=200,
            zoom=15,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()

    def get_distance(self, latitude_from, longitude_from, latitude_to, longitude_to):
        dx = (
            (longitude_to - longitude_from)
            * self.earth_radius
            * np.cos(latitude_from)
            * np.pi
            / 180
        )
        dy = (latitude_to - latitude_from) * self.earth_radius * np.pi / 180
        distance = np.sqrt(dx**2 + dy**2)
        return distance

    def get_infos_nearby(self, latitude, longitude, radius):
        # location = self.google_client.geocode(name)[0]["geometry"]["location"]
        location = {"lat": latitude, "lng": longitude}
        infos = []
        next_page_token = None
        while True:
            response = self.google_client.places_nearby(
                location=location,
                radius=radius,
                page_token=next_page_token,
            )
            infos.extend(response["results"])
            if "next_page_token" not in response.keys():
                break
            next_page_token = response["next_page_token"]
            time.sleep(5)
        return infos
    
    def add_place(self, place_id):
        response = self.google_client.place(place_id=place_id)
        self.infos.append(response['result'])
        self.drop_duplicates()
        self.save()

    def export_csv(self, filename):
        info_list = []
        for info in self.infos:
            if "rating" in info.keys():
                rating = info["rating"]
            else:
                rating = None
            info_list.append(
                {
                    "place_id": info["place_id"],
                    "name": info["name"],
                    "latitude": info["geometry"]["location"]["lat"],
                    "longitude": info["geometry"]["location"]["lng"],
                    "rating": rating,
                }
            )
        df = pd.DataFrame(info_list).drop_duplicates("place_id").reset_index(drop=True)
        df.to_csv(filename)
