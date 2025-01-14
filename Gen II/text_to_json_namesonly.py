import os
import json
from get_gen2_movelist import *

# Dictionary to store move names with the correct format (i.e., with spaces)
move_names = get_moves()

# Path to the folder containing the text files
folder_path = "/Users/jacob/Desktop/Pokemon-Learnset-Finder/Gen II/move_data"

# Dictionary to store all move data
moves_data = {}

def add_unique_to_list(item, target_list):
    """
    Add an item to the list only if it isn't already present.
    """
    if item not in target_list:
        target_list.append(item)

def parse_file(file_path):
    """
    Parse a single move text file and return its data as a list of Pokémon names, preserving order.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # List to store Pokémon names, preserving their order
    pokemon_list = []

    # Track the current section
    current_section = None

    # Parse lines
    for line in lines:
        line = line.strip()
        
        if line.startswith("Via Level Up:"):
            current_section = "Via Level Up"
        elif line.startswith("Via TM:"):
            current_section = "Via TM"
        elif line.startswith("Via Breeding:"):
            current_section = "Via Breeding"
        elif line.startswith("Via Special Event:"):
            current_section = "Via Special Event"
        elif line:  # If the line contains data
            if current_section == "Via Level Up":
                # Extract Pokémon names (no need for levels)
                parts = line.split(": Lv. ")
                if len(parts) > 1:
                    pokemon = parts[0].strip()
                    add_unique_to_list(pokemon, pokemon_list)
            elif current_section and line != "NONE":
                # Add Pokémon names for other sections
                add_unique_to_list(line.strip(), pokemon_list)

    # Return the ordered list of Pokémon names
    return pokemon_list


# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        curr_move = filename.replace(".txt", "")  # Use the filename (without .txt) as the move name
        move_name = move_names[curr_move]
        file_path = os.path.join(folder_path, filename)
        # Store the ordered Pokémon names for each move
        moves_data[move_name] = parse_file(file_path)

# Write the combined data to a JSON file
output_file = "/Users/jacob/Desktop/Pokemon-Learnset-Finder/webapp/movedata_namesonly.json"
with open(output_file, 'w') as json_file:
    json.dump(moves_data, json_file, indent=4)

print(f"Data has been successfully written to {output_file}")
