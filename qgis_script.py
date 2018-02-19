

import math
use = 150
p_instalacion = 1.0
factorMaligno = 1.0
for day in range(365):

    lluviaField = "p" + str(day).zfill(3) + "Mean"
    for manzana in manzana_layer:
        #expandedFeature(block).next()

        precipitacion = manzana.get(lluviaField)
        pop = manzana.get('pobtot')
        numeroDeInstalacionesPotenciales = manzana.get('n_inst_p')
        numeroDeInstalaciones = toInt(p_instalacion * numeroDeInstalacionesPotenciales)
        manzanaCapacityTank = numeroDeInstalaciones * 5000

        water_stored = manzana.get('w_stored')
        area_potencial = manzana.get('area_p')
        surface_used = p_instalacion * area_potencial
        water_today = factorMaligno * (precipitacion * surface_used) #en litros pues la precipitacion viene en milimetros y la surface_used en metros cuadrados, para un metro cuadrado un milimetro es un litro
        manzana.set('sum_used') += math.min(water_stored,(population * use) #se usa lo que hay y no mas
        manzana.set('water_stored') = math.max(0,math.min(manzanaCapacityTank, water_stored + water_today - (pop * use)))#se acumula lo que cae menos lo que se usa, con los limites entre 0 y manzanaCapacityTank
        if (manzana.get('water_stored') == manzanaCapacityTank):
            print manzana.get('CVEGEO'), "se llenó"
