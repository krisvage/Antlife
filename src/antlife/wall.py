class Wall:
  """ Location which is blocked by a wall
  """
  def __init__(self, Scenario, Name):
    self.Scenario = Scenario
    self.Name = Name
    self.FoodAmount = 0
    self.Location = (-1,-1)
    self.Radius = (Scenario.Parameter('WallSize')+1)//2
    self.Area = []

  def locate(self, Location = None):
    if Location:
      self.Location = Location
    return self.Location

  def __repr__(self):
    return "[%s, %s...]" % (self.Name, str(self.Area)[:22])
