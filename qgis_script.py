import numpy as np
from os.path import join
import math
import json
from os.path import dirname



#################### PARAMETROS ##################
volumenCisterna = 5000
areaCaptacion = 60.0
consumoPorPersona = 20
shape_path = r'/Users/fidel/Dropbox (LNCS)/EscenariosMarzo/escenario2/manzanas_consumo_20_test.shp'


factorEficiencia = 0.75
factorMaligno = 131.0625407
numeroDeDias = 361
folder = dirname(shape_path)

print folder
 
manzana_layer = QgsVectorLayer(shape_path, "manzanas", "ogr")
    
w_stored_array = np.zeros(numeroDeDias+1)
sum_used_array = np.zeros(numeroDeDias+1)

#para corerlo varios anios seguidos
#for manzana in manzana_layer.getFeatures():
#    w_stored_array[0] += manzana['w_stored'] 

manzana_layer.startEditing()

print "calculating  tank_cap, consumo, n_inst..."

contador = 0
#calcula  para cada manzana el numero de instalaciones: n_inst, la capacidad de almacenamiento: tank_cap, y el consumo por dia de habitantes de viviendas: consumo
for manzana in manzana_layer.getFeatures():
    contador += 1
    if contador % 6300 == 0:
        print str(contador / 630)+ "%"
    #print manzana['CVEGEO'], contador
    #determina el numero de instalaciones que caben y luego si el numero de viviendas en esa manzana es menor se queda con el numero de viviendas
    n_inst = math.trunc(manzana['area_p'] / areaCaptacion)
    if manzana['viv_hab'] < n_inst:
        n_inst = manzana['viv_hab']
    
    if manzana['ocup_viv'] == 0:
        n_inst = 0
    
    manzana['n_inst'] = n_inst
    
    
    
    manzana['tank_cap'] = n_inst * volumenCisterna
    manzana['consumo'] = n_inst * consumoPorPersona
    manzana['area_c'] = n_inst * areaCaptacion
    manzana_layer.updateFeature(manzana)
        

manzana_layer.commitChanges()


print "raining a year..."

manzana_layer.startEditing()
contador = 0   

for manzana in manzana_layer.getFeatures():
    #si no hay instalaciones en esta manzana no calcula nada
    contador += 1
    if contador % 6300 == 0:
        print str(contador / 630)+ "%"
    if manzana['n_inst'] > 0:
        water_stored = manzana['w_stored'] 
        sum_used = 0
        surface_used = manzana['area_c']
        manzanaCapacityTank = manzana['tank_cap']
        consumo = manzana['consumo']
        
        #print manzana['CVEGEO'], contador
        
        for day in range(1,numeroDeDias+1):
            
            lluviaField = "p" + str(day).zfill(3) + "mean"
          
            precipitacion = manzana[lluviaField]
            
            #el agua que callo este dia en la superficie de captacion 
            #en litros pues la precipitacion viene en milimetros y la surface_used en 
            #metros cuadrados, para un metro cuadrado un milimetro es un litro
            water_today = factorEficiencia * factorMaligno * (precipitacion * surface_used) 
    
            #se usa lo que hay y no mas
            sum_used += min(water_stored,consumo) 

            #se acumula lo que cae menos lo que se usa, con los limites entre 0 y manzanaCapacityTank
            water_stored = max(0, min(manzanaCapacityTank, water_stored + water_today - consumo))
           
            #estos arrays obtienen la suma para todas las manzanas del agua acumulada : w_stored y del agua aprovechada: sum_used para cada dia del anio
            sum_used_array[day] += sum_used
            w_stored_array[day] += water_stored
            
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
        

contador = 0
print "calculating percentage of comsumption from rain..."
#calcula p_lluvia que es el porcentaje del consumo anual que se cubriria con captacion de lluvia
for manzana in manzana_layer.getFeatures():
    contador += 1
    if contador % 6300 == 0:
        print str(contador / 630)+ "%"
    consumoAnual = numeroDeDias*consumoPorPersona*manzana['ocup_viv'] 
    if consumoAnual > 0:
        manzana['p_lluvia'] = 100 * (manzana['sum_used'] / consumoAnual)
    else:
        manzana['p_lluvia'] = 0
        
    manzana_layer.updateFeature(manzana)
        

manzana_layer.commitChanges()
