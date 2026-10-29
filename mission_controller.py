from pathfinding import bfs

class MissionController:
    def __init__(self, drone, environment):
        self.drone = drone
        self.environment = environment
        self.state = "IDLE"
        self.goal = None
        self.path = []
    
    def start_mission(self, goal):
        self.goal = goal

        start = self.drone.get_position()

        self.path = bfs(start, goal, self.environment)

        if self.path:
            self.state = "MOVING"
        else:
            self.state = "FAILED"

    def update(self):
        if self.state != "MOVING":
            return

        if self.drone.get_position() == self.goal:
            self.state = "COMPLETED"
            return

        if not self.environment.is_valid_move(self.path[1]):
            self.start_mission(self.goal)
            return

        if len(self.path) < 2:
            self.state = "FAILED"
            return

        self.drone.move_to(self.path[1])
        self.path.pop(0)

        if self.path[0] == self.goal:
            self.state = "COMPLETED"
            return
    
    def pause_mission(self):
        if self.state == "MOVING":
            self.state = "PAUSED"

    def resume_mission(self):
        if self.state == "PAUSED":
            self.state = "MOVING"
    
    def cancel_mission(self):
        self.goal = None
        self.path = []
        self.state = "IDLE"

    def reset_mission(self):
        self.goal = None
        self.path = []
        self.state = "IDLE"