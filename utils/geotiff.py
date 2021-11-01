import os
from io import BytesIO
import pandas as pd
import geopandas as gpd
from urllib.request import urlopen
from zipfile import ZipFile
import rioxarray
import rasterio
import rasterio.mask
from typing import List

class GeoTiff:
    # look for the right tif file
    def find_right_map(x: str, y: str) -> str:

        global number
        maps = pd.read_csv("data/tif_card_bounderies.csv")

        x_address = address_info["x_value"]
        y_address = address_info["y_value"]
        print(x_address, y_address)

        # for loop: if all of the if's returns True for a given row, than you have the right file
        for tif in range(maps.shape[0]):  # [0] indicates to the number of rows, while [1] refers to number of columns / shape:(43,5)
            if maps["xLeft"][tif] <= x_address:
                if maps["xRight"][tif] >= x_address:
                    if maps["yBottom"][tif] <= y_address:
                        if maps["yTop"][tif] >= y_address:
                            number = tif
                            break

        if number < 9:  # index 9 points to file number 10 / DSM_10
            num_tif_map = f"k0{number + 1}"  # add 1 to number to get the right map number
        else:
            num_tif_map = f"k{number + 1}"
        return num_tif_map

    # get the right maps
    def get_right_maps(number: str):

        url_dsm = f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_{num_tif_map}.zip"
        url_dtm = f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_{num_tif_map}.zip"

        zip_url = url_dsm

        for i in range(0, 1):
            with urlopen(zip_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    print(f"getting file: {zip_url}")
                    zfile.extractall(f'./data/temp/{zip_url[:3]}')
                    print(f"extraction done: {zip_url}")
            zip_url = url_dtm
        print("the tif files are extracted")

    def mask_tif_maps(number: str, polygon: List[str]) -> List[str]:
        # since the tif files are way to big and not right for the project
        # we crop a peace that only holds our address" polygon
        dsm_tif = f"./data/temp/dsm/GeoTiff/DHMVIIDSMRAS1m_{num_tif_map}"
        dtm_tif = f"./data/temp/dtm/GeoTiff/DHMVIIDTMRAS1m_{num_tif_map}"

        mask_files = []
        name = "dsm"

        for i in range(0, 1):
            data = rt.open(file)
            out_img, out_transform = mask(dataset=data, shapes=[polygon], crop=True)
            out_meta = data_meta.copy()
            epsg_code = int(data.crs.data['init'][5:])
            out_meta.update({"driver": "GTiff",
                             "heigth": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_transform,
                             "crs": epsg_code,
                             })
            with rt.open(f"./data/mask_file/{name}_mask.tif", "w", **out_meta) as dest_file:
                dest_file.write(out_img)
                print(name, "mask file is created")
                mask_files.append(f"./data/mask_file/{name}_mask.tif")
                shutil.rmtree(f"./data/temp/{name}/", ignote_errors=True)
                print(name, "file is deleted form the d")

            name = "dtm"
        return mask_files

    def get_canopy():
        dsm_tif = rt.open(mask_files[0])
        dsm_array = dsm_tif.read(1)
        dtm_tif = rt.open(mask_files[1])
        dtm_array = dtm_tif.read(1)
        canopy = dsm_array - dtm_array

        return canopy
