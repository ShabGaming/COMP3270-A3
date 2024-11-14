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

def format_grid_2(grid):
    # Helper function to format a single value
    def format_value(value):
        if value == '#':
            return " # "
        elif value == 'x':
            return " x "
        elif value == '':
            return "   "
        else:
            # Center-align the value with 1 spaces on either side
            return f" {value:^1} "
    rows = []
    for row in grid:
        # Format each value in the row
        formatted_row = [format_value(value) for value in row]
        # Join the formatted values with '||' as the central border
        rows.append(f"|{'||'.join(formatted_row)}|")
    # Join all rows with new lines
    return "\n".join(rows)