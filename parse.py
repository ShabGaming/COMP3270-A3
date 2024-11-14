def read_grid_mdp_problem_p1(file_path):
    # Initialize variables
    seed = None
    noise = None
    livingReward = None
    grid = []
    policy = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('seed:'):
            seed = int(line.split(':')[1].strip())
            i += 1
        elif line.startswith('noise:'):
            noise = float(line.split(':')[1].strip())
            i += 1
        elif line.startswith('livingReward:'):
            livingReward = float(line.split(':')[1].strip())
            i += 1
        elif line.startswith('grid:'):
            i += 1  # Skip 'grid:'
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith('policy:'):
                    break
                tokens = line.split()
                grid.append(tokens)
                i += 1
        elif line.startswith('policy:'):
            i += 1  # Skip 'policy:'
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    break
                tokens = line.split()
                policy.append(tokens)
                i += 1
        else:
            i += 1  # Skip unknown lines
    # Build the problem object
    problem = {
        'seed': seed,
        'noise': noise,
        'livingReward': livingReward,
        'grid': grid,
        'policy': policy
    }
    return problem

def read_grid_mdp_problem_p2(file_path):
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables
    grid = []
    policy = []
    reading_grid = False
    reading_policy = False

    for line in lines:
        line = line.strip()
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
        elif line.startswith('grid:'):
            reading_grid = True
            reading_policy = False
            continue
        elif line.startswith('policy:'):
            reading_grid = False
            reading_policy = True
            continue
        elif line == '':
            continue
        else:
            if reading_grid:
                grid_row = line.strip().split()
                grid.append(grid_row)
            elif reading_policy:
                policy_row = line.strip().split()
                policy.append(policy_row)
    
    problem['grid'] = grid
    problem['policy'] = policy
    return problem


def read_grid_mdp_problem_p3(file_path):
    problem = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Remove comments and empty lines
    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    
    # Parse parameters
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
        elif line.startswith('grid:'):
            # Read the grid lines
            grid = []
            i += 1
            while i < len(lines):
                grid_line = lines[i].strip()
                if grid_line:
                    # Split the grid line into cells
                    cells = grid_line.strip().split()
                    grid.append(cells)
                i += 1
            problem['grid'] = grid
            break  # No more lines after grid
        i += 1
    return problem

