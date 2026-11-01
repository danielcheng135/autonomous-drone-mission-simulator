
from environment import Environment
from pathfinding import bfs, astar


def run_test(name, environment, start, goal, expected_moves):
    print(f"\n--- {name} ---")

    bfs_path = bfs(start, goal, environment)
    astar_path = astar(start, goal, environment)

    print(f"BFS Path: {bfs_path}")
    print(f"A* Path:  {astar_path}")

    for algorithm, path in [("BFS", bfs_path), ("A*", astar_path)]:

        if expected_moves is None:
            assert path == [], f"{algorithm} should return no path"
            print(f"{algorithm}: PASS (no path found)")
            continue

        assert path, f"{algorithm} returned an empty path"
        assert path[0] == start, f"{algorithm} has incorrect start"
        assert path[-1] == goal, f"{algorithm} has incorrect goal"

        # Check that every move is valid and adjacent
        for current, next_position in zip(path, path[1:]):
            assert environment.is_valid_move(next_position), (
                f"{algorithm} moves into an invalid cell"
            )

            distance = (
                abs(next_position[0] - current[0])
                + abs(next_position[1] - current[1])
            )

            assert distance == 1, (
                f"{algorithm} makes a non-adjacent move"
            )

        moves = len(path) - 1

        assert moves == expected_moves, (
            f"{algorithm}: Expected {expected_moves} moves, got {moves}"
        )

        print(f"{algorithm}: PASS ({moves} moves)")


# Test 1: Original environment with obstacles
environment = Environment(7, 5)

environment.add_obstacle((3, 1))
environment.add_obstacle((3, 2))
environment.add_obstacle((3, 3))

run_test(
    "Original Environment",
    environment,
    (2, 3),
    (5, 4),
    4
)


# Test 2: Start and goal are the same
run_test(
    "Start Equals Goal",
    environment,
    (2, 3),
    (2, 3),
    0
)


# Test 3: Empty environment
empty_environment = Environment(7, 5)

run_test(
    "No Obstacles",
    empty_environment,
    (0, 0),
    (6, 4),
    10
)


# Test 4: Destination surrounded by obstacles
blocked_environment = Environment(7, 5)

blocked_environment.add_obstacle((2, 2))
blocked_environment.add_obstacle((4, 2))
blocked_environment.add_obstacle((3, 1))
blocked_environment.add_obstacle((3, 3))

run_test(
    "Unreachable Destination",
    blocked_environment,
    (0, 0),
    (3, 2),
    None
)


print("\nAll pathfinding tests passed!")
