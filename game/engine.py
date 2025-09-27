import json

def load_content(path):
    """
    Load the game content from JSON file

    Args:
        path (str): Path to the JSON file (e.g. "game/content.json")
    
    Returns:
        dict: parsed game content with rooms, start, and win condition.
    """

    with open(path) as f:
        content = json.load(f)

    if "rooms" not in content or "start" not in content:
        raise ValueError("Invalid game content: must contain 'rooms' and 'start'")
    
    return content

def new_state(content):
    """
    Initialize a new game state based on the provided content

    Args:
        content (dict): Parsed game content,typically loaded from content.json.
        Must contain a "start" key for the initial room.
    
    Returns:
        dict: A dictionary representing the player's current game state, with:
        - "current_room" (str): the name of the starting room.
        - "inventory" (list): an empty list for collected items.
        - "messages" (str): an empty string for status or feedback messages.
    """
    state = {}
    state["current_room"] = content["start"]
    state["inventory"] = []
    state["room_description"] = content["rooms"][state["current_room"]]["description"]
    state["messages"] = ""
    state["room_items"] = content["rooms"][state["current_room"]]["items"]
    state["room_exits"] = content["rooms"][state["current_room"]]["exits"]
    state["won"] = False
    state["dead"] = False
    return state

def parse_and_apply(state, command, content):
    """
    Parse the player's command and update the game state accordingly.

    Args:
        state (dict): The current game state, containing at least:
            - "current_room" (str): the player's current room.
            - "inventory" (list): items the player has collected.
            - "messages" (str): feedback from the last action.
        command (str): The raw text entered by the player (e.g. "north", "take torch").
        content (dict): The game world data loaded from content.json, containing rooms,
            descriptions, exits, and items.

    Returns: 
        state (dict): the updated game state after applying the command.
    """

    simple_command = command.lower().strip().split()
    if not simple_command:
        state["messages"] = "Enter a command"
        return state
    
    rooms = content["rooms"] # dictionary containing all rooms
    room = rooms[state["current_room"]] #dictionary of current room
    exits = room["exits"] # dictionary of current room's exits
    inventory = state["inventory"]
    if simple_command[0] =="look":
        if light_check(state["inventory"],room):
            if room["items"]:
                state["messages"] = f"This room contains {', '.join(room['items'])}"
            else:
                state["messages"] = "Nothing to collect here."
        else:
            state["messages"] = "The room is too dark. You need a torch."
        
    elif len(simple_command) == 2: 
        if simple_command[0] == "move" and simple_command[1] in exits:
            exit_taken = simple_command[1]
            if entrance_blocked(state["current_room"], exit_taken, inventory):
                state["messages"] = "You need a Key, a Firestone and a Relic to enter this Chamber."
                return state
            if inventory_error(exits[exit_taken], inventory):
                state["messages"] = "You can't enter this way carrying more than 2 items. Drop something first."
                return state
            next_room = rooms[exits[exit_taken]] # dictionary of the the next room if command is to move
            state["current_room"] = exits[exit_taken]
            state["messages"] = f"You have moved to the {state['current_room']}"
            state["room_description"] = next_room["description"]
            state["room_items"] = next_room["items"]
            state["room_exits"] = next_room["exits"]
        elif simple_command[0] == "move" and simple_command[1] in ["north", "east", "west", "south"]:
            state["messages"] = "You can't go that way"
        elif simple_command[1] in room["items"] and simple_command[0] == "take":
            item = simple_command[1]
            state["inventory"].append(item)
            room["items"].remove(item)
            state["messages"] = f"Collected {item}"
        elif  simple_command[1] in state["inventory"] and simple_command[0] == "drop":
            item = simple_command[1]
            state["inventory"].remove(item)
            room["items"].append(item)
            if item == "torch":
                state["messages"] = f"You dropped your {item}. Take it now or risk never seeing in the darkness again."
            else:
                state["messages"] = f"Dropped {item}"
        else:
            state["messages"] = "Command not understood"
    else:
        state["messages"] = "Command not understood"
        
    
    return state



# ----------HELPER Functions----------

def light_check(inventory,room):
    """check for torch and room condition and returns a boolean"""
    if room["dark"] == False:
        return True
    elif "torch" in inventory:
        return True
    return False
    

def entrance_blocked(room_name, exit, inventory):
    required = {"key", "firestone", "relic"}
    if room_name == "antechamber" and exit == "east":
        if not required.issubset(set(inventory)):
            return True
    if room_name == "shrine" and exit == "south":
        if not required.issubset(set(inventory)):
            return True
    return False

def inventory_error(exit_taken, inventory):
    if exit_taken == "narrow_passage" and len(inventory) > 2:
        return True
    return False

