from collections import deque
import heapq

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

def bfs(start, goal, environment, metrics=None):
    if not environment.is_valid_move(start):
        return []
    
    if not environment.is_valid_move(goal):
        return []

    queue = deque()
    visited = set()
    came_from = {}

    explored_count = 0

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()
        explored_count += 1

        if current == goal:            
            path = []
            position = goal

            path.append(position)

            while position != start:
                path.append(came_from[position])
                position = came_from[position]
            
            path.reverse()

            if metrics is not None:
                metrics["nodes_explored"] = explored_count

            return path

        neighbors = get_neighbors(current, environment)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    
    if metrics is not None:
        metrics["nodes_explored"] = 0
            
    return []

def astar(start, goal, environment, metrics=None):
    priority_queue = []

    g_score = {start: 0}
    came_from = {}

    explored_count = 0

    heapq.heappush(priority_queue, (heuristic(start, goal), start))
    while priority_queue:
        f_score, current_position = heapq.heappop(priority_queue)

        # Skip outdated queue entries
        expected_f_score = (
            g_score[current_position]
            + heuristic(current_position, goal)
        )

        if f_score > expected_f_score:
            continue

        # Count explored nodes
        explored_count += 1

        if current_position == goal:
            path = [goal]

            while current_position != start:
                path.append(came_from[current_position])
                current_position = came_from[current_position]

            path.reverse()

            if metrics is not None:
                metrics["nodes_explored"] = explored_count

            return path

        for neighbor in get_neighbors(current_position, environment):
            tentative_g_score = g_score[current_position] + 1
            previous_g_score = g_score.get(neighbor, float("inf"))

            if tentative_g_score < previous_g_score:
                came_from[neighbor] = current_position
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (f_score, neighbor))
    
    if metrics is not None:
        metrics["nodes_explored"] = 0
        
    return []

def heuristic(position, goal):
    x1, y1 = position
    x2, y2 = goal

    manhattan_distance = abs(y2 - y1) + abs(x2 - x1)

    return manhattan_distance