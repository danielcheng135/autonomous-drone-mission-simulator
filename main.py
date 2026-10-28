# from collections import deque

# width = 7
# height = 5

# drone_position = (2, 3)

# obstacles = {
#     (3, 1),
#     (3, 2),
#     (3, 3)
# }

# def is_valid_move(position, width, height, obstacles):
#     x, y = position

#     if 0 <= x < width and 0 <= y < height:
#         if position not in obstacles:
#             return True
    
#     return False

# def get_neighbors(position, width, height, obstacles):
#     neighbors = []

#     x, y = position

#     up = (x, y - 1)
#     down = (x, y + 1)
#     left = (x - 1, y)
#     right = (x + 1, y)

#     moves = [up, down, left, right]

#     for move in moves:
#         if (is_valid_move(move, width, height, obstacles)):
#             neighbors.append(move)

#     return neighbors

# def bfs(start, goal, width, height, obstacles):
#     queue = deque()
#     visited = set()
#     came_from = {}

#     queue.append(start)
#     visited.add(start)

#     while queue:
#         current = queue.popleft()
#         if current == goal:
#             print("Destination found!")
            
#             path = []
#             position = goal

#             path.append(position)

#             while position != start:
#                 path.append(came_from[position])
#                 position = came_from[position]
            
#             path.reverse()

#             return path

#         print(current)

#         neighbors = get_neighbors(current, width, height, obstacles)

#         for neighbor in neighbors:
#             if neighbor not in visited:
#                 queue.append(neighbor)
#                 visited.add(neighbor)
#                 came_from[neighbor] = current

#     return []

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

print("Drone position:", drone.get_position())
print("Shortest path:", path)
print("Number of moves:", len(path) - 1)