# PlaceExplorer
## Explore registered locations on Google Maps

### About
"PlaceExplorer" is a Python-based program that facilitates web scraping. It automatically collects information on registered locations from Google Maps, including the Place ID, latitude, longitude, review numbers, and rating of each location within a specified area. This allows users to obtain information on all places within an area of interest, as Google API only allows fetching of 60 randomly selected places.

### Installation

Follow these steps to clone and install the PlaceExplorer project:

1. Open a terminal window and navigate to the directory where you want to clone the repository.

2. Clone the GitHub repository by running the following command:

```bash
git clone https://github.com/TUCHIO/PlaceExplorer.git
```

3. Change into the newly created PlaceExplorer directory:

```bash
cd PlaceExplorer
```

4. Install the project using pip:

```bash
pip install .
```

### Preparation
To run the program, a Google Maps API key is required. The user must first specify three parameters: a center point (latitude and longitude), a radius (in meters) from the center, and a grid size (in meters) that represents the smallest unit of search within the radius. To prevent data loss in case of interruption, it is recommended to create a pickle file for saving the data.

#### API Key
You have to place a json file which includes following API Keys at `./examples/api_key.json`.
```json
{"google_api_key": "YOUR_GOOGLE_API_KEY", "outscraper_api_key": "YOUR_OUTSCRAPER_API_KEY"}
```
An easy start for Google Colaboratory user is [here](./docs/start_with_Google_Colaboratory.md). 

### Example Notebooks
#### [Basic usage of PE](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/basic_usage.ipynb)

The program searches for all places within the specified radius from the center (latitude and longitude) on Google Maps. An animation of the exploring process is available.

https://user-images.githubusercontent.com/108068990/203982433-69a83d6f-6512-4d95-8dd8-0700e244ca56.mp4

PE searches within the specified area by crawling from center to center. The search range will expand until at least 20 places are detected. As a result, large circles may be generated in uninhabited areas. Conversely, the search range will be narrowed to 60 or fewer places in densely populated areas, such as urban areas.

![show_centers](https://user-images.githubusercontent.com/108068990/203982670-a654f8ed-af4f-4a6a-b561-67310e87ae30.png)

Note that the size of the bubble displayed in the animation does not correspond to the actual searched area, but instead represents the relative radius (i.e., the bigger the bubble, the wider the search range, and the smaller the bubble, the narrower the search range).

#### [Recommended usage of PE](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/recommended_usage.ipynb)
By utilizing [Outscraper](https://outscraper.com/), users can obtain review number information for each place. This enables the program to plot large and small bubbles on a map based on the number of reviews within the search area. Moreover, users can access all reviews for each place in the searched area and download them in a CSV file.

The sample image shows a concentration of places in the only town on Easter Island. The large red bubbles represent World Heritage Sites on the island that have received many visitors and reviews. The vertical bar on the right displays the square root of the actual review numbers for each place. As a result, the large red bubbles correspond to approximately 1600-2500 reviews.

![Easterisland_Map](https://user-images.githubusercontent.com/108068990/203985845-89fe54b9-46b1-4103-a678-d27e9708f74d.png)


#### [Exploring multiple areas](https://github.com/TUCHIO/PlaceExplorer/blob/main/examples/explore_multiple_areas.ipynb)
Here is an applied use: PE allows you to explore and compare multiple areas. The search results will be merged into one csv file.

![newplot (6)](https://user-images.githubusercontent.com/108068990/203986093-5b9c6ffb-705f-4a7c-b043-a377de53f4f4.png)


