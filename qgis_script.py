

import math
use = 150
p_instalacion = 1.0
factorMaligno = 1.0

manzana_layer = QgsVectorLayer("/Users/fidel/Dropbox (LNCS)/beth/IslaUrbana/manzanas_censo_area_p.shp", "manzanas", "ogr")

for day in range(1,362):
    print day
    lluviaField = "p" + str(day).zfill(3) + "Mean"
    for manzana in manzana_layer.getFeatures():
      
        precipitacion = manzana[lluviaField]
        pop = manzana['pobtot']
        numeroDeInstalacionesPotenciales = manzana['n_inst_p']
        numeroDeInstalaciones = int(p_instalacion * numeroDeInstalacionesPotenciales)
        manzanaCapacityTank = numeroDeInstalaciones * 5000

        water_stored = manzana['w_stored']
        area_potencial = manzana['area_p']
        surface_used = p_instalacion * area_potencial
        water_today = factorMaligno * (precipitacion * surface_used) #en litros pues la precipitacion viene en milimetros y la surface_used en metros cuadrados, para un metro cuadrado un milimetro es un litro
        manzana_layer.startEditing()
        manzana['sum_used'] += min(water_stored,(pop * use)) #se usa lo que hay y no mas
        manzana['w_stored'] = max(0, min(manzanaCapacityTank, water_stored + water_today - (pop * use)))#se acumula lo que cae menos lo que se usa, con los limites entre 0 y manzanaCapacityTank
        manzana_layer.updateFeature(manzana)
        

        if (manzana['w_stored'] == manzanaCapacityTank and manzanaCapacityTank > 0):
            print manzana['CVEGEO'], "se lleno con ", manzanaCapacityTank
    manzana_layer.commitChanges()