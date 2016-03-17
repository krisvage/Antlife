import libs.Evolife.Ecology.Individual as EI
import random


# two functions to convert from complex numbers into (x,y) coordinates
c2t = lambda c: (int(round(c.real)),int(round(c.imag))) # converts a complex into a couple
t2c = lambda P: complex(*P) # converts a couple into a complex

class Ant(EI.Individual):
  """ Defines individual agents
  """
  def __init__(self, Scenario, Observer, PARAMS, Land, IdNb, InitialPosition):
    EI.Individual.__init__(self, Scenario, ID=IdNb)
    self.Observer = Observer
    self.PARAMS = PARAMS
    self.Land = Land
    self.Colony = InitialPosition # Location of the colony nest
    self.location = InitialPosition
    self.PPStock = self.Scenario.Parameter('PPMax') 
    self.Action = 'Move'
    self.moves()

  def Sniff(self):
    " Looks for the next place to go "
    Neighbourhood = self.Land.neighbours(self.location, self.Scenario.Parameter('SniffingDistance'))
    random.shuffle(Neighbourhood) # to avoid anisotropy
    acceptable = None
    best = -self.Scenario.Parameter('Saturation') # best == pheromone balance found so far
    for NewPos in Neighbourhood:
      # looking for position devoid of negative pheromon
      if NewPos == self.location: continue
      if self.Land.food(NewPos) > 0:
        # Food is always good to take
        acceptable = NewPos
        break
      found = self.Land.ppheromone(NewPos)   # attractiveness of positive pheromone
      found -= self.Land.npheromone(NewPos)   # repulsiveness of negative pheromone
      if found > best:        
        acceptable = NewPos
        best = found
    return acceptable

  def returnHome(self):
    " The ant heads toward the colony "
    Direction = t2c(self.Colony) - t2c(self.location)   # complex number operation
    Distance = abs(Direction)
    if Distance >= self.Scenario.Parameter('SniffingDistance'):
      # Negative pheromone
      if self.Scenario.Parameter('NPDeposit'):
        self.Land.npheromone(self.location, self.Scenario.Parameter('NPDeposit')) # marking current position as visited with negative pheromone
      # Positive pheromone
      self.Land.ppheromone(self.location, self.PPStock) # marking current posiiton as interesting with positive pheromone
      Direction /= Distance # normed vector
      # MaxSteps = int(Gbl.Parameter('LandSize') / 2 / Distance)  # 
      Decrease = int(self.PPStock / Distance) # Linear decrease
      self.PPStock -= Decrease
      # if self.PPStock <= Gbl.Parameter('PPMin'):   self.PPStock = Gbl.Parameter('PPMin')  # always lay some amount of positive pheromone
      self.location = c2t(t2c(self.location) + 2 * Direction) # complex number operation
      self.location = self.Land.ToricConversion(self.location)   # landscape is a tore
      self.Observer.recordChanges((self.ID, self.location + self.PARAMS.AntAspectWhenLaden)) # for ongoing display of ants
    else:
      # Home reached
      self.PPStock = self.Scenario.Parameter('PPMax') 
      self.Action = 'Move'
    
  def moves(self):
    """ Basic behavior: move by looking for neighbouring unvisited cells.
      If food is in sight, return straight back home.
      Lay down negative pheromone on visited cells.
      Lay down positive pheromone on returning home.
    """
    if self.Action == 'BackHome':
      self.returnHome()
    else:
      NextPos = self.Sniff()
      # print self.ID, 'in', self.location, 'sniffs', NextPos
      if NextPos is None or random.randint(0,100) < self.Scenario.Parameter('Exploration'): 
        # either all neighbouring cells have been visited or in the mood for exploration
        NextPos = c2t(t2c(self.location) + complex(random.randint(-1,1),random.randint(-1,1)))
        NextPos = self.Land.ToricConversion(NextPos)
      # Marking the old location as visited
      if self.Scenario.Parameter('NPDeposit'):
        self.Land.npheromone(self.location, self.Scenario.Parameter('NPDeposit'))
        # Observer.recordChanges(('NP%d_%d' % self.location, self.location + NPAspect)) # for ongoing display of negative pheromone

      # print("\n\n-----------------\n\n")
      # print(NextPos)
      # print(self.Land.WallPos)
      if NextPos not in self.Land.WallPos:
        self.location = NextPos
      # else:
      #   print('Blocked by wall')

      if self.Land.food(self.location) > 0:  
        self.Land.food(self.location, -1)  # consume one unit of food
        self.Observer.FoodCollected += 1
        self.Action = 'BackHome'  # return when having found food
      self.Observer.recordChanges((self.ID, self.location + self.PARAMS.AntAspect)) # for ongoing display of ants

  def position(self):
    return c2t(self.Position)
