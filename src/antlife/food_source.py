class FoodSource:
  """ Location where food is available
  """
  def __init__(self, Scenario, Name):
    self.Scenario = Scenario
    self.Name = Name
    self.FoodAmount = 0
    self.Location = (-1,-1)
    self.Radius = (Scenario.Parameter('FoodSourceSize')+1)//2
    self.Distribution = Scenario.Parameter('FoodQuantity') // ((2*self.Radius+1) ** 2)
    self.Area = []

  def locate(self, Location = None):
    if Location:
      self.Location = Location
    return self.Location

  def __repr__(self):
    return "[%s, %d, %s...]" % (self.Name, self.FoodAmount, str(self.Area)[:22])
