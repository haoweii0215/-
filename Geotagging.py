import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon

## Read location data
df = pd.read_csv('location.csv')
df.replace({np.nan:None}, inplace=True)

## Translate to Point
def tran_point(r):
    return Point(r['經度'], r['緯度'])

df['Point'] = df.apply(tran_point, 1)

## Read geojson
sf = gpd.read_file(r"E:\Python\營業商家資料\商圈標記資料\TWBusinessDistinct.geojson", encoding='utf-8')

## Convert to dictionary
geodata = {}

for i in tqdm(range(len(sf))):
    c, name, g = sf['縣市'][i], sf['商圈名稱'][i], sf['geometry'][i]
    if c not in geodata.keys():
        geodata[c] = [(name, g)]
    else:
        geodata[c].append((name, g))

## Tag distinct
def distinct_mark(r):
    if r['Point'] :
        data = geodata[r['縣市']]
        tmp = []
        for x in data:
            ans = x[1].contains(r['Point'])
            if ans == True:
                tmp.append(x[0])
            else:
                pass
        if tmp:
            return tmp
        else:
            return None
    else:
        return None

df['Business Distinct'] = df.apply(distinct_mark, 1)