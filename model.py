from decimal import Decimal
from datetime import date

from pony.orm import *

db = Database()

class Block(db.Entity):
    """
    Model of a city block.

    Blocks have surfaces that collect rainwater in their tanks.
    Tanks fill up with this water, and drain with usage by population.

    For any given day the model reports usage of water from the tank.
    """
    id = PrimaryKey(int, auto=True)    
    population = Required(Decimal)
    use = Required(Decimal)  # water usage by populator
    surface_available = Required(Decimal)
    surface_used = Required(Decimal)    
    tank_capacity = Required(Decimal)
    water_stored = Required(Decimal)

    precipitation = Set('Precipitation')
    def next(self, precipitacion):
        """
        water stored on next time step
        """
        self.water_stored = math.min(self.water_stored + (precipitacion * self.surface_used)
                                     - (self.population * self.use), self.tank_capacity)

    def tank_usage(self, day):
        pass

class Precipitation(db.Entity):
    """
    For a given block and a given day, how much rain from the sky has
    fallen?
    """
    block = Required('Block')
    day = Required(date)
    volume = Required(Decimal)    


set_sql_debug(True)
db.bind('sqlite', 'model.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
