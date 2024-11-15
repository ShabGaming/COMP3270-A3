import sys, grader, parse
import copy

def value_iteration(problem):
    # Extract parameters from problem
    grid = problem['grid']
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations = problem['iterations']
    
    # Grid dimensions
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Actions
    actions = ['N', 'S', 'W', 'E']
    action_indices = {'N': 0, 'S': 1, 'W': 2, 'E': 3}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E
    
    # Map to store V(s)
    V = {}
    policy = {}  # Policy map
    
    # Map to store the type of each cell
    # Also, collect all the states
    states = []
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell != '#':
                state = (i, j)
                states.append(state)
                V[state] = 0.0  # Initialize V(s) = 0.0
    
    # Get terminal states and their rewards
    terminal_states = {}
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if isinstance(cell, str) and cell.isnumeric():
                reward = float(cell)
                terminal_states[(i, j)] = reward
    
    return_value = ''
    # Output V_k=0
    return_value += f"V_k=0\n"
    return_value += format_values(V, grid) + '\n'
    
    for k in range(iterations):
        V_new = copy.deepcopy(V)
        for state in states:
            if state in terminal_states:
                V_new[state] = terminal_states[state]
                policy[state] = 'x'  # Terminal states have no policy
            else:
                max_value = float('-inf')
                best_action = None
                for a in actions:
                    value = 0.0
                    transitions = get_transitions(state, a, grid, noise, livingReward, terminal_states)
                    for (prob, next_state, reward) in transitions:
                        value += prob * (reward + discount * V[next_state])
                    if value > max_value:
                        max_value = value
                        best_action = a
                V_new[state] = max_value
                policy[state] = best_action
        V = copy.deepcopy(V_new)
        
        # Format and append the outputs
        return_value += f"V_k={k+1}\n"
        return_value += format_values(V, grid) + '\n'
        return_value += f"pi_k={k+1}\n"
        return_value += format_policy(policy, grid) + '\n'
    
    return return_value.strip()  # Remove the trailing newline

def get_transitions(state, action, grid, noise, livingReward, terminal_states):
    actions = ['N', 'S', 'W', 'E']
    action_indices = {'N': 0, 'S': 1, 'W': 2, 'E': 3}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    intended_index = action_indices[action]
    intended_direction = directions[intended_index]
    # Perpendicular directions
    left_index = (intended_index - 1) % 4
    right_index = (intended_index + 1) % 4
    perpendicular_indices = [left_index, right_index]
    
    # Probabilities according to problem description
    intended_prob = 1 - 2 * noise
    perpendicular_prob = noise
    
    transitions = []
    
    # Intended action
    next_state = move(state, intended_direction, grid)
    reward = get_reward(state, next_state, livingReward, terminal_states)
    transitions.append((intended_prob, next_state, reward))
    
    # Perpendicular actions
    for idx in perpendicular_indices:
        direction = directions[idx]
        next_state = move(state, direction, grid)
        reward = get_reward(state, next_state, livingReward, terminal_states)
        transitions.append((perpendicular_prob, next_state, reward))
    
    return transitions

def move(state, direction, grid):
    rows = len(grid)
    cols = len(grid[0])
    i, j = state
    di, dj = direction
    new_i = i + di
    new_j = j + dj
    if 0 <= new_i < rows and 0 <= new_j < cols:
        if grid[new_i][new_j] != '#':
            return (new_i, new_j)
    return state  # If move is into wall or outside grid, stay in same state

def get_reward(state, next_state, livingReward, terminal_states):
    if state in terminal_states:
        return 0  # No reward if starting from terminal state
    if next_state in terminal_states:
        return terminal_states[next_state]
    else:
        return livingReward

def format_values(V, grid):
    rows = len(grid)
    cols = len(grid[0])
    formatted_rows = []
    for i in range(rows):
        row_values = []
        for j in range(cols):
            cell = grid[i][j]
            if cell == '#':
                value_str = " ##### "
            else:
                state = (i, j)
                value = V[state]
                value_str = f"{value:7.2f}"
            row_values.append(value_str)
        formatted_row = "|{}|".format('||'.join(row_values))
        formatted_rows.append(formatted_row)
    return '\n'.join(formatted_rows)

def format_policy(policy, grid):
    rows = len(grid)
    cols = len(grid[0])
    formatted_rows = []
    for i in range(rows):
        row_values = []
        for j in range(cols):
            cell = grid[i][j]
            if cell == '#':
                value_str = " # "
            else:
                state = (i, j)
                action = policy.get(state, '')
                value_str = f" {action} "
            row_values.append(value_str)
        formatted_row = "|{}|".format('||'.join(row_values))
        formatted_rows.append(formatted_row)
    return '\n'.join(formatted_rows)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
