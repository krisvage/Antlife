import libs.Evolife.Ecology.Group as EG
from src.antlife.ant import Ant
# import libs.Evolife.Ecology.Population as EP


class Group(EG.Group):
  # The group is a container for individuals.
  # Individuals are stored in self.members

  def __init__(self, Scenario, Observer, PARAMS, ColonyPosition, Land, ID=1, Size=100):
    self.Observer = Observer
    self.PARAMS = PARAMS
    self.ColonyPosition = ColonyPosition
    self.Land = Land
    EG.Group.__init__(self, Scenario, ID=ID, Size=Size)
    
  def createIndividual(self, ID=None, Newborn=True):
    # calling local class 'Individual'
    return Ant(self.Scenario, self.Observer, self.PARAMS, self.Land, self.free_ID(Prefix='A'), self.ColonyPosition)  # call to local class 'Ant'
