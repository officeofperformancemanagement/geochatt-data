# /// script
# dependencies = [
#   "requests",
#   "shapely",
# ]
# ///

import array
from collections import Counter
import csv
import gzip
import io
import json
import math
import zipfile

import requests
import shapely

csv.field_size_limit(2147483647)  # maximum value of a long

data = requests.get(
    "https://raw.githubusercontent.com/officeofperformancemanagement/live-parcels/refs/heads/main/live_parcels.geojson.zip"
).content

with zipfile.ZipFile(io.BytesIO(data)) as z:
    text = z.read(z.namelist()[0])

inFeatureCollection = json.loads(text)

outFeatureCollection = {"type": "FeatureCollection", "features": []}

for feature in inFeatureCollection["features"]:
    address = feature["properties"].get("ADDRESS")
    if address:
        outFeatureCollection["features"].append(
            {
                "type": "Feature",
                "properties": {"ADDRESS": address},
                "geometry": feature["geometry"],
            }
        )

# with open("./files/live_parcels.geojson", "wt", newline="") as f:
#     json.dump(outFeatureCollection, f)

with gzip.open("./files/live_parcels.geojson.gz", "wt", newline="") as f:
    json.dump(outFeatureCollection, f)

with zipfile.ZipFile(
    "./files/live_parcels.geojson.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as zip_file:
    dumped = json.dumps(outFeatureCollection, ensure_ascii=False)
    zip_file.writestr("live_parcels.geojson", data=dumped)
