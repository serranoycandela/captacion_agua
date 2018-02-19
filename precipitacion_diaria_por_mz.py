from os import listdir
from os.path import join
from qgis.analysis import QgsZonalStatistics
p_folder = "/Users/fidel/Dropbox (LNCS)/precipitacion_por_dia/"
vlayer = QgsVectorLayer("/Users/fidel/Dropbox (LNCS)/beth/IslaUrbana/manzanas_censo_area_p.shp", "manzanas", "ogr")
for raster in sorted(listdir(p_folder)):
    if raster.endswith("tif"):
        dia = raster.split(".")[0]
        print dia, join(p_folder, raster)
        zoneStat = QgsZonalStatistics (vlayer, join(p_folder, raster), dia, 1, QgsZonalStatistics.Mean)
        zoneStat.calculateStatistics(None)
#
#zoneStat = QgsZonalStatistics (vlayer, "/Users/fidel/Dropbox (LNCS)/to_fidel_utm/Radares0101.tif", "_", 1, QgsZonalStatistics.Mean)
#zoneStat.calculateStatistics(None)