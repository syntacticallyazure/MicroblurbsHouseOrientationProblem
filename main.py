import ijson
import json
from shapely.geometry import shape, Point
import requests

#probably make this a .env
# https://www.kaggle.com/datasets/joebeachcapital/australia-building-footprints
# the data was retrieved from Kaggle, originating from Microsoft's Image Recognition AI.
DATA_FILE = './data/Australia.geojson'

# reads the file and returns all "features" aka houses as a generator.
def feature_generator(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for feature in ijson.items(f, "features.item"):
            yield feature

#when provided a lon and lat, as well as a file, check if that point falls within the boundaries dictated within the file.
def is_point_in_feature(lon, lat, file_path):
    counter = 1
    """
    Check if a point (lon, lat) falls within any feature in the GeoJSON file.
    """
    point = Point(lon, lat)
    for feature in feature_generator(file_path):
        geom = shape(feature['geometry'])
        if geom.contains(point):
            print("Found it on the {}th run!".format(counter))
            print(f"House's plot points are: {feature}")
            return True
        counter = counter + 1
    return False

#boilerplate code to fetch from an API, extract the long and lat and run them through the above two functions.
url = "https://www.microburbs.com.au/report_generator/api/suburb/properties"
params = {
    "suburb": "Belmont North"
}
headers = {
    "Authorization": "Bearer test",
    "Content-Type": "application/json"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()

for real_estate_property in data["results"]:
    print(f"Processing: {real_estate_property["address"]["street"] + " " + real_estate_property["address"]["sal"]}")
    print(f"At provided long/lat: " + json.dumps(real_estate_property.get("coordinates")))
    is_point_in_feature(real_estate_property.get("coordinates")["longitude"], real_estate_property.get("coordinates")["latitude"], './data/Australia.geojson')
    break

#TODO: There are multiple ways to go about doing this.
# - You could assume that the face of the house is always the longest side. But that is not perfect.
# - The flawless method is to determine the coordinates of the provided road and return coordinates that are closest to the house; the side that is the closest, must be the face, and the orientation would also be solved.