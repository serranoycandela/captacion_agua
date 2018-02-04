from decimal import Decimal
from datetime import date

from pony.orm import *

db = Database()

class Block(db.Entity):
    id = PrimaryKey(int, auto=True)    
    population = Required(Decimal)
    use = Required(Decimal)
    surface_available = Required(Decimal)
    surface_used = Required(Decimal)    
    tank_capacity = Required(Decimal)
    water_stored = Required(Decimal)

    precipitation = Set('Precipitation')

    def tank_usage(self, day):
        pass

class Precipitation(db.Entity):
    block = Required('Block')
    day = Required(date)
    volume = Required(Decimal)    


set_sql_debug(True)
db.bind('sqlite', 'model.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
