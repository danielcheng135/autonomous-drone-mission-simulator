class Drone:
    def __init__(self, position):
        self.position = position
    
    def move_to(self, destination):
        self.position = destination
    
    def get_position(self):
        return self.position