class Drone:
    def __init__(self, position):
        self.position = position
    
    def move_to(self, destination):
        self.position = destination
    
    def get_position(self):
        return self.position

drone = Drone((2, 3))

print("Starting position:", drone.get_position())

drone.move_to((2, 4))
print("After moving down:", drone.get_position())

drone.move_to((3, 4))
print("After moving right:", drone.get_position())