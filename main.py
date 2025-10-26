import ijson
import json

#probably make this a .env
DATA_FILE = './data/Australia.geojson'

def feature_generator(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for feature in ijson.items(f, "features.item"):
            yield feature

# for feature in feature_generator('./data/Australia.geojson'):
#     print(feature)
#     break

from shapely.geometry import shape, Point

def is_point_in_feature(lon, lat, file_path):
    counter = 1
    """
    Check if a point (lon, lat) falls within any feature in the GeoJSON file.
    """
    point = Point(lon, lat)
    for feature in feature_generator(file_path):
        geom = shape(feature['geometry'])
        if geom.contains(point):
            print("Found it on the {}th".format(counter))
            return True
        counter = counter + 1
    return False


# # Example usage
# lon, lat = 151.67272249, -33.01402088  # Sydney coordinates
# if is_point_in_feature(lon, lat, './data/Australia.geojson'):
#     print("Point is inside a shape!")
# else:
#     print("Point is outside all shapes.")

import requests

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

for real_estate_property in data:
    print(real_estate_property)