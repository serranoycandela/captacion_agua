import processing
from os import  listdir
from os.path import join

original_folder = "/Users/fidel/Dropbox (LNCS)/to_fidel/"
new_folder = "/Users/fidel/Dropbox (LNCS)/to_fidel_utm/"
folders = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

contador = 0
for subfolder in folders:
    subfolder_path = join(original_folder,subfolder)
    for raster in sorted(listdir(subfolder_path)):
        if raster.endswith("tiff"):
            contador += 1
            print str(contador).zfill(3), join(subfolder_path, raster)
            processing.runalg("gdalogr:warpreproject",
                                  {"INPUT":join(subfolder_path, raster),
                                  "SOURCE_SRS":"EPSG:4326 ",
                                  "DEST_SRS":"EPSG:32614",
                                  "NO_DATA":"-9999",
                                  "METHOD":0,
                                  "RTYPE":5,
                                  "COMPRESS":0,
                                  "BIGTIFF":2,
                                  "OUTPUT":join(new_folder, "p"+ str(contador).zfill(3) + ".tif") })
                                  
#processing.runalg("gdalogr:warpreproject",
#                                  {"INPUT": "/Users/fidel/Dropbox (LNCS)/to_fidel/01/Radares0101.tiff",
#                                  "SOURCE_SRS":"EPSG:4326 ",
#                                  "DEST_SRS":"EPSG:32614",
#                                  "NO_DATA":"-9999",
#                                  "METHOD":0,
#                                  "RTYPE":5,
#                                  "COMPRESS":0,
#                                  "BIGTIFF":2,
#                                  "OUTPUT":"/Users/fidel/Dropbox (LNCS)/to_fidel_utm/Radares0101.tif" })