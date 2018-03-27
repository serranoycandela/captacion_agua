import numpy as np
from os.path import join
import math
import json
use = 20
p_instalacion = 1.0
factorEficiencia = 0.75
factorMaligno = 131.0625407
volumenCisterna = 5000

folder = "/Users/fidel/Dropbox (LNCS)/EscenariosMarzo/escenario2"
manzana_layer = QgsVectorLayer("/Users/fidel/Dropbox (LNCS)/EscenariosMarzo/escenario2/manzanas_consumo_20.shp", "manzanas", "ogr")
    
    
    
w_stored_array = np.zeros(362)
sum_used_array = np.zeros(362)

for manzana in manzana_layer.getFeatures():
    w_stored_array[0] += manzana['w_stored'] 

print "starting..."

manzana_layer.startEditing()
contador = 0   

for manzana in manzana_layer.getFeatures():
    water_stored = manzana['w_stored'] 
    sum_used = 0
    surface_used = manzana['area_c']
    manzanaCapacityTank = manzana['tank_cap']
    consumo = manzana['consumo']
    contador += 1
    print manzana['CVEGEO'], contador
    
    for day in range(1,362):
        
        lluviaField = "p" + str(day).zfill(3) + "mean"
      
        precipitacion = manzana[lluviaField]
        #pop = manzana['pobtot']
 
        

        #water_stored = manzana['w_stored']
        #area_potencial = manzana['area_p']
        #surface_used = p_instalacion * area_potencial
        #surface_used = 60 * numeroDeInstalaciones
        
        water_today = factorEficiencia * factorMaligno * (precipitacion * surface_used) #en litros pues la precipitacion viene en milimetros y la surface_used en metros cuadrados, para un metro cuadrado un milimetro es un litro
        
        sum_used += min(water_stored,consumo) #se usa lo que hay y no mas
        water_stored = max(0, min(manzanaCapacityTank, water_stored + water_today - consumo))#se acumula lo que cae menos lo que se usa, con los limites entre 0 y manzanaCapacityTank
        
        sum_used_array[day] += sum_used
        w_stored_array[day] += water_stored
        #manzana['sum_used'] += min(water_stored,consumo) #se usa lo que hay y no mas
        #manzana['w_stored'] = max(0, min(manzanaCapacityTank, water_stored + water_today - consumo))#se acumula lo que cae menos lo que se usa, con los limites entre 0 y manzanaCapacityTank
        
    manzana['sum_used'] = sum_used
    manzana['w_stored'] = water_stored
    manzana_layer.updateFeature(manzana)
        

manzana_layer.commitChanges()
try:
    with open(join(folder,'sum_used_array.json'), 'w') as outfile:
        json.dump(list(sum_used_array), outfile)
        
    with open(join(folder,'w_stored_array.json'), 'w') as outfile:
        json.dump(list(w_stored_array), outfile)
        
except:
    print "no pude"
        

