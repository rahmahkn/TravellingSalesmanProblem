class Coordinate():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    # Function to count Euclidean Distance between 2 coordinates
    def eucDistance(self, otherCoor):
        return ((otherCoor.x-self.x)**2 + (otherCoor.y-self.y)**2)** 0.5