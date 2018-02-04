



for day in year:
    for block in block_layer:
        #expandedFeature(block).next()
        precipitacion = getPrecipitacion(block.get('id'),day)
        population = block.get('populatuon')
        tank_capacity = block.get('tank_capacity')
        water_stored = block.get('water_stored')
        surface_used = block.get('surface_used')
        block.set('water_stored') = water_stored + (preciìtacion * surface_used) - (population * use)
        