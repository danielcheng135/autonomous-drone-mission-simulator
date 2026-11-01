from pathfinding import bfs, astar
import time

class MissionController:
    def __init__(self, drone, environment):
        self.drone = drone
        self.environment = environment
        self.state = "IDLE"
        self.algorithm = "BFS"
        self.goal = None
        self.path = []
        self.nodes_explored = 0
        self.search_time_ms = 0.0

    def calculate_path(self, start, goal, metrics=None):
        if self.algorithm == "BFS":
            return bfs(start, goal, self.environment, metrics)
        else:
            return astar(start, goal, self.environment, metrics)
    
    def start_mission(self, goal):
        self.goal = goal

        start = self.drone.get_position()

        metrics = {}
        start_time = time.perf_counter()

        self.path = self.calculate_path(start, goal, metrics)

        self.search_time_ms = (time.perf_counter() - start_time) * 1000
        self.nodes_explored = metrics.get("nodes_explored", 0)

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

        if len(self.path) < 2:
            self.state = "FAILED"
            return

        if not self.environment.is_valid_move(self.path[1]):
            self.start_mission(self.goal)
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

        self.nodes_explored = 0
        self.search_time_ms = 0.0

    def reset_mission(self):
        self.goal = None
        self.path = []
        self.state = "IDLE"

        self.nodes_explored = 0
        self.search_time_ms = 0.0