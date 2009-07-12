from librpg.map import *
from librpg.util import *
from librpg.party import *

import pygame

pygame.init()

m = Map(MapModel('maptest.map', ('lower_tileset.png', 'lower_tileset.bnd'), ('upper_tileset.png', 'upper_tileset.bnd')))

print m.map_model

print 'Terrain layer:'
print m.map_model.terrain_layer

print 'Scenario layer:'
print m.map_model.scenario_layer

r = CharacterReserve()
a = Character('Andy', 'char_alex.png')
r.add_char(a)
p = r.create_party(3)
p.add_char(a)

print 'Adding', str(p)
m.map_model.add_party(p, Position(0, 0))
print 'Added'
print

print 'Trying to add', str(p), 'again'
try:
    m.map_model.add_party(p, Position(0, 0))
except AssertionError:
    print 'Ooops, map already had a party'
print

print 'Removing party'
party, pos = m.map_model.remove_party()
print 'Removed', party, pos
print

print 'Trying to remove party again'
party, pos = m.map_model.remove_party()
print 'Removed', party, pos
print

print 'Adding', str(p)
m.map_model.add_party(p, Position(0, 0), Direction.RIGHT, MapObject.SLOW_SPEED)
print 'Added'
print

print 'Starting gameloop()'
m.gameloop()
print 'Finished gameloop()'

exit()