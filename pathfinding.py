from collections import deque

def get_neighbors(position, environment):
    neighbors = []

    x, y = position

    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)

    moves = [up, down, left, right]

    for move in moves:
        if (environment.is_valid_move(move)):
            neighbors.append(move)

    return neighbors

def bfs(start, goal, environment):
    if not environment.is_valid_move(start):
        return []
    
    if not environment.is_valid_move(goal):
        return []

    queue = deque()
    visited = set()
    came_from = {}

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            
            path = []
            position = goal

            path.append(position)

            while position != start:
                path.append(came_from[position])
                position = came_from[position]
            
            path.reverse()

            return path

        neighbors = get_neighbors(current, environment)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

    return []