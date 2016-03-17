import libs.Evolife.Other.Landscapes as Landscapes


class LandCell(Landscapes.LandCell):
  """ Defines what's in one location on the ground
  """

  # Cell content is defined as a triple  (Food, NegativePheromon, PositivePheromon)

  def __init__(self, F=0, NP=0, PP=0):
    Landscapes.LandCell.__init__(self, (0, 0), VoidCell=(0, 0, 0))
    self.setContent((F,NP,PP))

  def clean(self):  
    return self.setContent((self.Content()[0],0,0))

  def food(self, addendum=0): 
    (F,NP,PP) = self.Content()
    if addendum:  self.setContent((F + addendum, NP, PP))
    return F + addendum
    
  def np(self, Scenario, addendum=0): 
    (F,NP,PP) = self.Content()
    if addendum:  self.setContent((F, self.limit(Scenario, NP + addendum), PP))
    return NP + addendum

  def pp(self, Scenario, addendum=0): 
    (F,NP,PP) = self.Content()
    if addendum:  self.setContent((F, NP, self.limit(Scenario, PP + addendum)))
    return PP + addendum

  def limit(self, Scenario, Pheromone):
    return min(Pheromone, Scenario.Parameter('Saturation'))

  # def __add__(self, Other):
    # # redefines the '+' operation between cells
    # return LandCell(self.food()+Other.food(),
            # self.limit(self.np() + Other.np()),
            # self.limit(self.pp() + Other.pp())

  def evaporate(self, Scenario):
    # Pheromone evaporation should be programmed about here
    if self.np(Scenario) > 0:
      self.np(Scenario, addendum=-Gbl.Parameter('Evaporation')) # Repulsive ('negative') pheromone
    if self.pp(Scenario) > 0:
      self.pp(Scenario, addendum=-Gbl.Parameter('Evaporation')) # Attractive ('positive') Pheromone
    if self.np(Scenario) <= 0 and self.pp(Scenario) <= 0:
      self.clean()
      return True
    return False
