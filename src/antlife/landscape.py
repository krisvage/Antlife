import random

import libs.Evolife.Other.Landscapes as Landscapes

# from libs.Evolife.Other.Landscapes import LandCell
from src.antlife.land_cell   import LandCell
from src.antlife.food_source import FoodSource
from src.antlife.wall        import Wall


class Landscape(Landscapes.Landscape):
  """ A 2-D grid with cells that contains food or pheromone
  """
  def __init__(self, Scenario, Observer, PARAMS):
    Size = Scenario.Parameter('LandSize')
    NbFoodSources = Scenario.Parameter('NbFoodSources')
    NbWalls = Scenario.Parameter('NbWalls')

    food_sources = Scenario.Parameter('FoodSources')

    coords = [point.split(';') for point in food_sources.split('|')]
    food_sources_locations = [((int(c[0].split(',')[0]), int(c[0].split(',')[1])), (int(c[1].split(',')[0]), int(c[1].split(',')[1]))) for c in [xy for xy in coords]]

    walls = Scenario.Parameter('Walls')

    coords = [point.split(';') for point in walls.split('|')]
    wall_locations = [((int(c[0].split(',')[0]), int(c[0].split(',')[1])), (int(c[1].split(',')[0]), int(c[1].split(',')[1]))) for c in [xy for xy in coords]]

    self.Scenario = Scenario
    self.Observer = Observer
    self.PARAMS = PARAMS

    Landscapes.Landscape.__init__(self, Size, CellType=LandCell)

    # Positioning Food Sources
    self.FoodSourceNumber = NbFoodSources
    self.FoodSources = []
    for FSn, xy in enumerate(food_sources_locations):
      x, y = xy
      FS = FoodSource(Scenario, 'FS%d' % FSn)
      FS.locate((x[0] * Size / x[1], y[0] * Size / y[1]))
      self.FoodSources.append(FS)
      for Pos in self.neighbours(FS.locate(), Radius=FS.Radius):
        FS.Area.append(Pos)
        self.food(Pos, FS.Distribution)  # Cell contains a certain amount of food
      self.Observer.recordChanges((FS.Name, FS.locate() + PARAMS.FoodAspect)) # to display food sources

    # Positioning walls
    self.WallPos = []
    for Wn, xy in enumerate(wall_locations):
      W = Wall(Scenario, 'W%d' % Wn)
      x, y = xy
      wall_pos = (x[0] * Size / x[1], y[0] * Size / y[1])
      W.locate(wall_pos)
      self.WallPos.append(wall_pos)

      for Pos in self.neighbours(W.locate(), Radius=W.Radius):
        W.Area.append(Pos)
        self.WallPos.append(Pos)

      self.Observer.recordChanges((W.Name, W.locate() + PARAMS.WallAspect))

  # def Modify(self, (x,y), Modification):
    # self.Ground[x][y] += Modification   # uses addition as redefined in LandCell
    # return self.Ground[x][y]

  # def FoodSourceConsistency(self):
    # for FS in self.FoodSources:
      # amount = 0
      # for Pos in FS.Area:
        # amount += self.food(Pos)
      # if amount != FS.FoodAmount:
        # print('************ error consistency %s: %d %d' % (FS.Name, amount, FS.FoodAmount))
        # print [self.food(Pos) for Pos in FS.Area]
        # FS.FoodAmount = amount
            
  def food(self, Pos, delta=0):
    if delta:
      # let the food source know
      for FS in self.FoodSources:
        if Pos in FS.Area:
          FS.FoodAmount += delta
          if FS.FoodAmount <= 0:
            self.Observer.recordChanges((FS.Name, FS.locate() + self.PARAMS.FoodDepletedAspect)) # to display food sources
    return self.Cell(Pos).food(delta) # adds food
  
  def foodQuantity(self):
    return sum([FS.FoodAmount for FS in self.FoodSources])
  
  def npheromone(self, Pos, delta=0): 
    if delta: 
      self.ActiveCells.append(Pos)
      self.Observer.recordChanges(('NP%d_%d' % Pos, Pos + self.PARAMS.NPAspect)) # for ongoing display of negative pheromone
    return self.Cell(Pos).np(delta) # adds repulsive pheromone
    
  def ppheromone(self, Pos, delta=0): 
    if delta:
      self.ActiveCells.append(Pos)
      self.Observer.recordChanges(('PP%d_%d' % Pos, Pos + self.PARAMS.PPAspect)) # for ongoing display of positive pheromone
    return self.Cell(Pos).pp(delta) # adds attractive pheromone

  def evaporation(self):
    for Pos in self.ActiveCells.list()[:]:
      if self.Cell(Pos).evaporate(self.Scenario): # no pheromone left
        # call 'erase' for updating display when there is no pheromone left
        self.erase(Pos) # for ongoing display
        self.ActiveCells.remove(Pos)

  def erase(self, Pos):
    " says to Observer that there is no pheromon left at that location "
    self.Observer.recordChanges(('NP%d_%d' % Pos, Pos + (-1,))) # negative colour means erase from display
    self.Observer.recordChanges(('PP%d_%d' % Pos, Pos + (-1,))) # negative colour means erase from display
    
  def update_(self):
    # scans ground for food and pheromone - May be used for statistics
    Food = NPher = PPher = []
    for (Position, Cell) in Land.travel():
      if Cell.Food:   Food.append((Pos, Cell.food()))
      if Cell.NPheromone: NPher.append((Pos, Cell.np()))
      if Cell.PPheromone: PPher.append((Pos, Cell.pp()))
    return (Food, NPher, PPher)
