#!/usr/bin/env python
# coding=utf-8

""" Collective foraging:
Though individual agents follow erratic paths to find food,
the collective may discover optimal paths.
"""

__author__ = 'Dessalles'

## Modified by Kristian Våge (NTNU) during Athens Week March 2016

##############################################################################
# EVOLIFE  www.dessalles.fr/Evolife                    Jean-Louis Dessalles  #
#            Telecom ParisTech  2014                       www.dessalles.fr  #
##############################################################################

##############################################################################
# Ants                                                                       #
##############################################################################

# In this story, 'ants' move in search for food
# In the absence of pheromone, ants move randomly for some time,
# and then head back toward the colony.
# When they find food, they return to the colony while laying down pheromone.
# If they find pheromone, ants tend to follow it.


#######     NOTE:  this is just a sketch. The programme must be completed to
#######     display appropriate behaviour


import sys
from time import sleep
import random

sys.path.append('libs')

import Evolife.Scenarii.Parameters as EPar
import Evolife.QtGraphics.Evolife_Window as EW

from src.antlife.ant_observer import AntObserver
from src.antlife.landscape    import Landscape
from src.antlife.population   import Population

from src.antlife.hardcoded_params import HardcodedParams

import res.imgs.ants as imgs

#################################################
# Aspect of ants, food and pheromons on display
#################################################
AntAspect = ('black', 6)  # 6 = size
AntAspectWhenLaden = ('red1', 7)  # 6 = size
FoodAspect = ('yellow', 14)
WallAspect = ('red', 70)
FoodDepletedAspect = ('brown', 14)
PPAspect = (17, 2)  # 17th colour
NPAspect = ('blue', 2)

PARAMS = HardcodedParams(AntAspect, AntAspectWhenLaden, FoodAspect, WallAspect, FoodDepletedAspect, PPAspect, NPAspect)

if __name__ == "__main__":
  print(__doc__)

  #############################
  # Global objects      #
  #############################

  cfg = sys.argv[1]

  Gbl = EPar.Parameters(cfg)  # Loading global parameter values
  Observer = AntObserver(Gbl)   # Observer contains statistics
  Land = Landscape(Gbl, Observer, PARAMS)
  Pop = Population(Gbl, Observer, PARAMS, Land)   # Ant colony
  Observer.recordChanges(('Dummy', (Gbl.Parameter('LandSize'), Gbl.Parameter('LandSize'), 0, 1)))  # to resize the field

  Observer.recordInfo('FieldWallpaper', list(imgs.__path__)[0] + '/Grass1.jpg')

  EW.Start(Pop.One_Decision, Observer, Capabilities='RPC')

  print("Bye.......")
  sleep(1.0)
