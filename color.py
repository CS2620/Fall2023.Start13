import math

class Color:
  
  def __init__(self, color):
    self.r = color[0]
    self.g = color[1]
    self.b = color[2]

  
  def scale(self, scalar):
    return Color([self.r * scalar, self.g * scalar, self.b * scalar])
  
  
  def add(self, color):
    return Color([self.r + color.r, self.g + color.g, self.b + color.b])

  def asList(self):
    return (int(math.floor(self.r)), int(math.floor(self.g)), int(math.floor(self.b)), 255)