import time
import tracemalloc

from src.map_data import MapData

def measure_memory_and_time(func):
    """
    Decorator to measure the memory and time usage of the search algorithm.
    """
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_usage = peak_memory / (1024 * 1024)  # Convert to MB
        time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, time_taken, memory_usage
    return wrapper

def generate_new_state(state, direction, map_matrix, stones_weight):
    """
    Generate a new state based on the current state and the direction.
    """
    current_position, stones_positions, path, weight_pushed = state

    move_symbol = {
        (0, 1): "r",
        (0, -1): "l",
        (1, 0): "d",
        (-1, 0): "u"
    }[direction]

    rows, cols = len(map_matrix), len(map_matrix[0])

    new_position = (current_position[0] + direction[0], current_position[1] + direction[1])

    if not (0 <= new_position[0] < rows and 0 <= new_position[1] < cols):
        return None
    if map_matrix[new_position[0]][new_position[1]] == MapData.BLOCKER:
        return None

    new_stones_positions = list(stones_positions)

    if new_position in stones_positions:
        stone_index = stones_positions.index(new_position)
        new_stone_position = (new_position[0] + direction[0], new_position[1] + direction[1])

        if not (0 <= new_stone_position[0] < rows and 0 <= new_stone_position[1] < cols):
            return None
        if (map_matrix[new_stone_position[0]][new_stone_position[1]] == MapData.BLOCKER or
                new_stone_position in stones_positions):
            return None

        weight_pushed += stones_weight[stone_index]
        new_stones_positions[stone_index] = new_stone_position
        move_symbol = move_symbol.upper()

    new_path = path + [move_symbol]
    return new_position, tuple(new_stones_positions), new_path, weight_pushed

def check_if_reach_goal_state(state, goal_state):
    """
    Check if the current state matches the goal state.
    """
    _, stones_positions, _, _ = state
    _, goal_stones_positions = goal_state
    # Convert both to lists for comparison
    return list(stones_positions) == list(goal_stones_positions)
