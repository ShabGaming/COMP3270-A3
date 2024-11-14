import sys, grader, parse

def play_episode(problem):
    # Extract the problem components
    seed = problem['seed']
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid_array = problem['grid']  # list of lists
    policy_array = problem['policy']  # list of lists

    # Initialize the random number generator
    if seed != -1:
        import random
        random.seed(seed, version=1)

    # Process the grid to create a 2D array, find start state
    num_rows = len(grid_array)
    num_cols = len(grid_array[0])  # assuming rectangular grid

    # Find the start state
    start_state = None
    for i in range(num_rows):
        for j in range(num_cols):
            if grid_array[i][j] == 'S':
                start_state = (i, j)
    if start_state is None:
        raise Exception("Start state not found")

    # Initialize the cumulative reward
    cumulative_reward = 0.0
    experience = ''

    # Function to print the grid with the agent's position
    def print_grid(agent_pos, show_agent=True):
        output = ''
        for i in range(num_rows):
            row_output = '    '  # 4 spaces at the start of each line
            for j in range(num_cols):
                cell_content = grid_array[i][j]
                if (i, j) == agent_pos and show_agent:
                    cell = 'P'
                else:
                    cell = cell_content
                if j < num_cols - 1:
                    # Not the last column
                    cell_str = '{:<5}'.format(cell)  # Fixed width of 5
                else:
                    # Last column
                    if len(cell) >= 2:
                        # Value length is 2: left-align within 4 characters
                        cell_str = '{:<4}'.format(cell)
                        row_output = row_output[:-(len(cell)-1)]  # Remove the extra space
                    else:
                        # Other cases: left-align within 5 characters
                        cell_str = '{:<5}'.format(cell)
                row_output += cell_str
            output += row_output.rstrip() + '\n'
        return output.rstrip()
    
    def print_grid(agent_pos, show_agent=True):
        output = ''
        for i in range(num_rows):
            row_output = ''  # 4 spaces at the start of each line
            if len(grid_array[i][0]) > 1:
                row_output = row_output[:-(len(cell_content) - 1)]
            for j in range(num_cols):
                cell_content = grid_array[i][j]
                if (i, j) == agent_pos and show_agent:
                    cell = 'P'
                else:
                    cell = cell_content
                cell = " " * (5 - len(cell)) + cell
                row_output += cell
            output = output + row_output + '\n'
        return output.rstrip()

    # Function to format numbers appropriately
    def format_number(num):
        num = round(num + 1e-8, 2)
        if num == int(num):
            return str(int(num)) + '.0'
        else:
            return str(num)

    # Output the start state
    experience += 'Start state:\n'
    experience += print_grid(start_state) + '\n'
    experience += 'Cumulative reward sum: {}\n'.format(format_number(cumulative_reward))
    experience += '-------------------------------------------- \n'

    # Begin the episode
    current_state = start_state
    terminal = False
    while not terminal:
        # Get the intended action from the policy
        i, j = current_state
        intended_action = policy_array[i][j]
        current_cell = grid_array[i][j]
        if intended_action == 'exit':
            try:
                # Attempt to parse the current cell's value as float
                reward = float(current_cell)
                cumulative_reward += reward
                # Output the action, reward, new state, cumulative reward
                experience += 'Taking action: {} (intended: {})\n'.format('exit', 'exit')
                experience += 'Reward received: {}\n'.format(format_number(reward))
                experience += 'New state:\n'
                # After exiting, the agent is no longer on the grid
                experience += print_grid(current_state, show_agent=False) + '\n'
                experience += 'Cumulative reward sum: {}'.format(format_number(cumulative_reward))
                terminal = True
            except ValueError:
                # If the current cell is not a numerical terminal state, cannot exit
                experience += 'Attempted to exit from a non-terminal cell.\n'
                experience += 'Cumulative reward sum: {}'.format(format_number(cumulative_reward))
                # Optionally, you can choose to end the episode or handle it differently
                terminal = True  # To prevent infinite loop
        else:
            # Determine the actual action taken, considering noise
            actual_action = get_actual_action(intended_action, noise)
            # Compute the next state
            next_state = get_next_state(current_state, actual_action, grid_array)
            # Get the reward
            reward = livingReward
            cumulative_reward += reward
            # Output the action, reward, new state, cumulative reward
            experience += 'Taking action: {} (intended: {})\n'.format(actual_action, intended_action)
            experience += 'Reward received: {}\n'.format(format_number(reward))
            experience += 'New state:\n'
            experience += print_grid(next_state) + '\n'
            experience += 'Cumulative reward sum: {}\n'.format(format_number(cumulative_reward))
            experience += '-------------------------------------------- \n'
            # Update the current state
            current_state = next_state
    return experience.rstrip()

# Helper functions
def get_actual_action(intended_action, noise):
    import random
    d = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    weights = [1 - 2 * noise, noise, noise]
    actual_action = random.choices(population=d[intended_action], weights=weights)[0]
    return actual_action

def get_next_state(current_state, action, grid_array):
    num_rows = len(grid_array)
    num_cols = len(grid_array[0])
    i, j = current_state
    action_effects = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    if action not in action_effects:
        return current_state
    di, dj = action_effects[action]
    new_i = i + di
    new_j = j + dj
    if new_i < 0 or new_i >= num_rows or new_j < 0 or new_j >= num_cols:
        return current_state
    if grid_array[new_i][new_j] == '#':
        return current_state
    else:
        return (new_i, new_j)

def get_reward(current_state, intended_action, grid_array, livingReward):
    i, j = current_state
    current_cell = grid_array[i][j]
    if intended_action == 'exit':
        try:
            return float(current_cell)
        except ValueError:
            return 0.0  # Or handle as needed
    else:
        return livingReward

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
