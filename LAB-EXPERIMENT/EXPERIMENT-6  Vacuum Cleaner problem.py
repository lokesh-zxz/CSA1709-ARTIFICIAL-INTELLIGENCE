def perceive(location, status):
    """
    Returns the current percept: (location, status[location])
    """
    return (location, status[location])


def rules_match(state):
    """
    Simple rule‑based agent for the 2‑location vacuum world.
    Returns an action based on the current percept.
    """
    loc, clean = state
    if clean == 'Dirty':
        return 'Suck'          
    elif loc == 'A':
        return 'Right'        
    elif loc == 'B':
        return 'Left'          
    else:
        return 'NoOp'         


def update_location(loc, action):
    """Update the vacuum's location based on the action."""
    if action == 'Right':
        return 'B'
    elif action == 'Left':
        return 'A'
    else:
        return loc  


def update_status(loc, action, status):
    """Update the cleanliness status after an action."""
    if action == 'Suck':
        status = status.copy()
        status[loc] = 'Clean'
    return status


def run_vacuum(initial_loc, initial_status, steps=10):
    """
    Simulate the vacuum agent for a given number of steps.
    Prints each step so you can see what the agent does.
    """
    loc = initial_loc
    status = dict(initial_status)
    print(f"Initial state: Vacuum at {loc}, Status = {status}")
    for step in range(1, steps + 1):
        percept = perceive(loc, status)
        action = rules_match(percept)
        print(f"Step {step:2d}: Percept {percept} -> Action {action}")

        if action == 'Suck':
            status = update_status(loc, action, status)
        else:
            loc = update_location(loc, action)

        print(f"          -> New state: Vacuum at {loc}, Status = {status}\n")

        if all(v == 'Clean' for v in status.values()):
            print("All squares are clean. Stopping.")
            break


if __name__ == "__main__":
    start_location = 'A'
    start_status   = {'A': 'Dirty', 'B': 'Dirty'}

    run_vacuum(start_location, start_status, steps=15)
