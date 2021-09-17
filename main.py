from random import Random, SystemRandom, randrange
from time import sleep, time, ctime
import sys

class Map():
  def __init__(self):
    # Ask for map parameters
    x = 40
    y = 20
    self.coord = x, y
    self.Map = []
    for xi in range(0, x):
      self.Map.append([])
      for yi in range(0, y):
        self.Map[xi].append([0, 0, [0, 0]])
    
    self.modCleanerThreshold = 5
    
  def createSeed(self):
    x, y = self.coord
    self.seed = str(randrange(10**10, 10**15))
    while True:
      if len(self.seed) < (x*y):
        self.seed += str(randrange(10**20, 10**30))
      elif len(self.seed) >= (x*y):
        break
  
  def generateMap(self):
    x, y = self.coord
    mapChance = []
    modNatChance = 0.25
    modInfluencedChance = 0.75
    modDiagnalInfluence = 0
    #noiseLevel = 50
    seed = self.seed
    #mapChance Initialization
    for xi in range(0, x):
      mapChance.append([])
      for yi in range(0, y):
        mapChance[xi].append([0, 0])
    
    #NatChance Attribute
    for yi in range(0, y):
      for xi in range(0, x):
        natChance = int(modNatChance * (int(seed[int(yi+xi)]) * 10))
        mapChance[xi][yi][0] = natChance
    
    #InfluencedChance Attribute
    for yi in range(0, y):
      for xi in range(0, x):
        try:
          ax0 = mapChance[int(xi+1)][yi][0]
        except:
          ax0 = 0
        try:
          ax1 = mapChance[int(xi-1)][yi][0]
        except:
          ax1 = 0
        try:
          ax2 = mapChance[xi][int(yi+1)][0]
        except:
          ax2 = 0
        try:
          ax3 = mapChance[xi][int(yi-1)][0]
        except:
          ax3 = 0
        try:
          per0 = modDiagnalInfluence * mapChance[int(xi+1)][int(yi+1)][0]
        except:
          per0 = 0
        try:
          per1 = modDiagnalInfluence * mapChance[int(xi+1)][int(yi-1)][0]
        except:
          per1 = 0
        try:
          per2 = modDiagnalInfluence * mapChance[int(xi-1)][int(yi+1)][0]
        except:
          per2 = 0
        try:
          per3 = modDiagnalInfluence * mapChance[int(xi-1)][int(yi-1)][0]
        except:
          per3 = 0
        influencedChance = int(modInfluencedChance * (ax0 + ax1 + ax2 + ax3 + per0 + per1 + per2 + per3))
        mapChance[xi][yi][1] = influencedChance
    
    #Map Tile Definer
    for yi in range(0, y):
      for xi in range(0, x):
        tempVal = int(mapChance[xi][yi][0] + mapChance[xi][yi][1])
        noiseLevel = randrange(0, 101)
        if tempVal < noiseLevel:
          self.Map[xi][yi][0] = 0
        elif tempVal >= noiseLevel:
          self.Map[xi][yi][0] = 1
    self.printMap()
    sleep(1)
  
  def mapCleaner(self, modCleanerThreshold):
    if type(modCleanerThreshold) == int:
      self.modCleanerThreshold = modCleanerThreshold
    #Map Cleaner
    x, y = self.coord
    for yi in range(0, y):
      for xi in range(0, x):
        #Creates Border
        if xi == 0 or yi == 0 or xi == int(x - 1) or yi == int(y - 1):
          self.Map[xi][yi][0] = 1
        # Modifies Internal Map
        else:
          solidCount = 0
          for subxi in range(-1, 2):
            for subyi in range(-1, 2):
              if self.Map[int(xi + subxi)][int(yi + subyi)][0] == 1:
                if subxi == 0 and subyi == 0:
                  continue
                else:
                  solidCount += 1
          if int(solidCount) < self.modCleanerThreshold:
            self.Map[xi][yi][0] = 0
          elif int(solidCount) >= self.modCleanerThreshold:
            self.Map[xi][yi][0] = 1
          else:
            print('Error')
    
    self.printMap()
    sleep(1)
    
    #Todo: Define the starting and ending point
    
    #Todo: Define values dependant upon their location relative to the end point
  
  #def solveMap(self):
    #Todo: A* Algorithm to find solution
  
  #def updateValues(self):
    #Todo: Update distance-from-start values
    
  def printMap(self):
    # X is untested
    # O is an obstacle
    # F is discovered
    # P is the path
    x, y = self.coord
    for yi in range(0, y):
      tempMap = ''
      for xi in range(0, x):
        tempVal = self.Map[xi][yi][0]
        if tempVal == 0:
          tempMap += '\u001b[43mX'
          continue
        elif tempVal == 1:
          tempMap += '\u001b[47mO'
          continue
        elif tempVal == 2:
          tempMap += '\u001b[43mx'
          continue
        elif tempVal == 3:
          tempMap += '\u001b[45mP'
          continue
        else:
          print('Error: Value Unknown')
          pass
      
      print(tempMap)
    sys.stdout.write("\u001b[1000D" + "\u001b[1000A")
    sys.stdout.flush()
    #print('\n \n')


x = Map()
x.createSeed()
x.generateMap()
for I in range(0, 3):
  x.mapCleaner(False)