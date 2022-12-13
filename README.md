# PlaceExplorer
## Explore registered locations on Google Maps

### About
“PlaceExplorer” is Python-based program for web scraping. PE provides automatic collection of information on registered locations on Google Maps. The acquired information contains the Place ID, latitude, longitude, review numbers, and rating from each of locations within the specified area.
The purpose is to enable you to get the information of all places in an area where you want to search because Google API allows you to fetch only 60 places at random in the area.

### Preparation
Google Maps API Key is necessary to run the program. 
The users firstly set three parameters: a center point (Latitude and Longitude) , a radius (m) from the center, and a grid size (m) as the smallest unit of search within the radius. 
Creating a pickle file is recommended to save the data at the time of interruption and restart.

#### API Key
You have to place a json file which includes following API Keys at `./examples/api_key.json`.
```json
{"google_api_key": "YOUR_GOOGLE_API_KEY", "outscraper_api_key": "YOUR_OUTSCRAPER_API_KEY"}
```
An easy start for Google Colaboratory user is [here](./docs/start_with_Google_Colaboratory.md). 

### Example Notebooks
#### [Basic usage of PE](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/basic_usage.ipynb)

It searches all places on Google Maps within the specified area (radius) from the center (latitude and longitude).
Here is an animation of the exploring process

https://user-images.githubusercontent.com/108068990/203982433-69a83d6f-6512-4d95-8dd8-0700e244ca56.mp4

PE crawls within the area for search from center to center. The search range will expand until at least 20 places are detected. So it tends to be large circles in uninhabited areas. Conversely, the search range will be shrank to 60 or less places where many places are densely located, such as urban areas.

![show_centers](https://user-images.githubusercontent.com/108068990/203982670-a654f8ed-af4f-4a6a-b561-67310e87ae30.png)

The size of bubble does not match the actual searched area, but it shows relative radius (the bigger the wider, the smaller the narrower). 

#### [Recommended usage of PE](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/recommended_usage.ipynb)
By utilizing [Outscraper](https://outscraper.com/), you can get the review number information of each place. It enables you to plot large and small bubbles on a map based on the number of reviews in a search area. In addition, you will be able to get all reviews of all places in the searched area and download them in csv file. 

Here is the sample image. Places are concentrated in the only town on Easter Island. The large red bubbles are World Heritage Sites on the Island where many people visited and posted the reviews. The vertical bar on the right shows the square root of the actual review numbers for each place. Thus these large red bubbles are equal to about 1600〜2500 reviews there.

![Easterisland_Map](https://user-images.githubusercontent.com/108068990/203985845-89fe54b9-46b1-4103-a678-d27e9708f74d.png)


#### [Exploring multiple areas](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/explore_multiple_areas.ipynb)
Here is an applied use: PE allows you to explore and compare multiple areas. The search results will be merged into one csv file.

![newplot (6)](https://user-images.githubusercontent.com/108068990/203986093-5b9c6ffb-705f-4a7c-b043-a377de53f4f4.png)


