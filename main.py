from drone import Drone
from environment import Environment
from pathfinding import bfs

environment = Environment(7, 5)

environment.add_obstacle((3, 1))
environment.add_obstacle((3, 2))
environment.add_obstacle((3, 3))

drone = Drone((2, 3))
goal = (5, 4)

path = bfs(drone.get_position(), goal, environment)

if path:
    for position in path[1:]:
        drone.move_to(position)
        print(f"Drone moved to: {drone.get_position()}")

    print("Mission completed!")
else:
    print("Mission failed: No available route.")