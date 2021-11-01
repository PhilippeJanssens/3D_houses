# import the necessary packages
from shapely.geometry import Polygon
import plotly.graph_objects as go
import time
from utils.api import API
from utils.geotiff import GeoTiff

address = input("Enter your addess in 'Vlaanderen': ")
start = time.time()

address_info = API.get_address_data_from_geopunt(address)
polygon = address_info["polygon"][0]["coordinates"][0]

number = GeoTiff.find_right_map(address_info["x_value"] ,address_info["y_value"])

GeoTiff.get_right_maps(number)
mask_files = GeoTiff.mask_tif_maps(number, polygon)

canopy = GeoTiff.get_canopy(mask_files)

image = go.Figure(data=go.Surface(z=canopy))
image.update_layout(f"3D representation of {address}")
image.show()
image.write_image(f"data/3D-images/{address}.png")
end = time.time()
print(f"processing time: {end - start}")
