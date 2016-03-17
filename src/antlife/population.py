import libs.Evolife.Ecology.Population as EP

from src.antlife.group import Group


class Population(EP.Population):
  " defines the population of agents "
  
  def __init__(self, Scenario, Observer, PARAMS, Land):
    self.Observer = Observer
    self.PARAMS = PARAMS
    self.Land = Land
    self.ColonyPosition = (Scenario.Parameter('LandSize')//2, Scenario.Parameter('LandSize')//2)
    EP.Population.__init__(self, Scenario, Observer)
    " creates a population of ant agents "
    self.AllMoved = 0  # counts the number of times all agents have moved on average
    self.SimulationEnd = 400 * self.popSize
    # allows to run on the simulation beyond stop condition

  def createGroup(self, ID=0, Size=0):
    return Group(self.Scenario, self.Observer, self.PARAMS, self.ColonyPosition, self.Land, ID=ID, Size=Size)  # Call to local class 'Group'

  def One_Decision(self):
    """ This function is repeatedly called by the simulation thread.
      One ant is randomly chosen and decides what it does
    """
    EP.Population.one_year(self)  # performs statistics
    ant = self.selectIndividual()
    ant.moves()
    Moves = self.year // self.popSize # One step = all Walkers have moved once on average
    # print (self.year, self.AllMoved, Moves),
    if Moves > self.AllMoved:
      self.Land.evaporation()
      self.AllMoved = Moves
    if (self.Land.foodQuantity() <= 0):  self.SimulationEnd -= 1
    return self.SimulationEnd > 0  # stops the simulation when True
