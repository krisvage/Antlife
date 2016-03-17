import Evolife.Ecology.Observer as EO


class AntObserver(EO.Observer):
  """ Stores global variables for observation
  """
  def __init__(self, Scenario):
    EO.Observer.__init__(self, Scenario)
    self.CurrentChanges = []  # stores temporary changes
    self.recordInfo('CurveNames', [('yellow', 'Year (each ant moves once a year on average)\n\t\tx\n\t\tAmount of food collected')])
    self.FoodCollected = 0

  def recordChanges(self, Info):
    # stores current changes
    # Info is a couple (InfoName, Position) and Position == (x,y) or a longer tuple
    self.CurrentChanges.append(Info)

  def get_info(self, Slot, default=None):
    " this is called when display is required "
    if Slot == 'PlotOrders':  return [('yellow', (self.StepId // self.Scenario.Parameter('PopulationSize'), self.FoodCollected))] # curve
    else: return EO.Observer.get_info(self, Slot, default=default)
    
  def get_data(self, Slot):
    if Slot == 'Positions':
      CC = self.CurrentChanges
      # print CC
      self.CurrentChanges = []
      return tuple(CC)
    else: return EO.Observer.get_data(self, Slot)
