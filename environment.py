class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()
    
    def add_obstacle(self, position):
        self.obstacles.add(position)
    
    def is_valid_move(self, position):
        x, y = position

        if 0 <= x < self.width and 0 <= y < self.height:
            if position not in self.obstacles:
                return True
        
        return False

environment = Environment(7, 5)

environment.add_obstacle((3, 1))
environment.add_obstacle((3, 2))
environment.add_obstacle((3, 3))

print(environment.is_valid_move((2, 4)))
print(environment.is_valid_move((3, 3)))
print(environment.is_valid_move((7, 2)))
print(environment.is_valid_move((0, 0)))