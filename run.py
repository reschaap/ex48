#!/usr/bin/env python

from ex48.game import *

a_map = Map('laser_weapon_armory')
a_game = Engine(a_map)
a_game.play()