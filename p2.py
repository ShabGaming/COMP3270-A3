import sys, grader, parse

def policy_evaluation(problem):
    # Extract parameters
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']
    
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Initialize value function V(s) to zero for all states
    V = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Identify terminal states and their rewards
    terminal_states = {}
    for y in range(num_rows):
        for x in range(num_cols):
            cell = grid[y][x]
            if cell not in ['_', 'S', '#', '#####']:
                try:
                    reward = float(cell)
                    terminal_states[(y, x)] = reward
                except ValueError:
                    pass  # Ignore non-reward cells

    outputs = []
    for k in range(iterations):
        # Print V(s)
        outputs.append(f"V^pi_k={k}")
        formatted_grid = []
        for y in range(num_rows):
            formatted_row = []
            for x in range(num_cols):
                cell = grid[y][x]
                if cell == '#' or cell == '#####':
                    formatted_row.append('#####')
                else:
                    val = V[y][x]
                    formatted_row.append("{0:7.2f}".format(val))
            formatted_grid.append(formatted_row)
        outputs.append(format_grid(formatted_grid))

        V_new = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]
        for y in range(num_rows):
            for x in range(num_cols):
                s = (y, x)
                cell = grid[y][x]
                action = policy[y][x]
                if cell == '#' or cell == '#####' or action == '#':
                    V_new[y][x] = V[y][x]  # Do not update walls
                elif s in terminal_states:
                    V_new[y][x] = terminal_states[s]
                else:
                    V_new[y][x] = compute_state_value(s, V, grid, policy, discount, noise, livingReward, terminal_states)
        V = V_new

    return '\n'.join(outputs)

def compute_state_value(s, V, grid, policy, discount, noise, livingReward, terminal_states):
    num_rows = len(grid)
    num_cols = len(grid[0])
    y, x = s
    action = policy[y][x]
    # Skip walls and invalid actions
    if action == 'exit' or action == '#' or grid[y][x] == '#' or grid[y][x] == '#####':
        return V[y][x]  # Should not update walls or terminal states

    directions = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    left_turn = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}
    right_turn = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

    intended_prob = 1 - 2 * noise
    side_prob = noise

    transitions = []

    # Intended move
    dy, dx = directions.get(action, (0, 0))
    new_y, new_x = y + dy, x + dx
    if is_valid_state(new_y, new_x, grid):
        transitions.append(((new_y, new_x), intended_prob))
    else:
        transitions.append(((y, x), intended_prob))
    
    # Side moves
    for side_action in [left_turn.get(action, action), right_turn.get(action, action)]:
        dy, dx = directions.get(side_action, (0, 0))
        side_y, side_x = y + dy, x + dx
        if is_valid_state(side_y, side_x, grid):
            transitions.append(((side_y, side_x), side_prob))
        else:
            transitions.append(((y, x), side_prob))
    
    # Compute expected value
    expected_value = 0.0
    for (new_y, new_x), prob in transitions:
        reward = livingReward
        expected_value += prob * (reward + discount * V[new_y][new_x])
    return expected_value

def is_valid_state(y, x, grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    if 0 <= y < num_rows and 0 <= x < num_cols:
        cell = grid[y][x]
        if cell != '#####' and cell != '#':
            return True
    return False

def format_grid(grid):
    # Helper function to format a single value
    def format_value(value):
        if value == "#####":
            # Center ##### with one space on each side
            return " ##### "
        else:
            # Right-align the value in 7-character space
            return f"{value:>7}"
        
    rows = []
    for row in grid:
        # Format each value in the row
        formatted_row = [format_value(value) for value in row]
        # Join the formatted values with '||' as the central border
        rows.append(f"|{'||'.join(formatted_row)}|")
    
    # Join all rows with new lines
    return "\n".join(rows)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)
