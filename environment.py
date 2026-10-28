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
