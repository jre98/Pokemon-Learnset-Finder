import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import os
import re

# Import helper functions
from extract_helper_funcs import *

# Import function that will get the list of all moves from Gen II
from get_gen2_movelist import get_moves

# Dictionary containing all moves from the Gen II Pokemon Games
all_moves = {}

# List containing the HM moves that have the possiblity to come up. In these
# cases, we want to change what is written to the text file for the title for
# TM vs HM, as they are labeled the same in the HTML
HM_moves = ["surf", "whirlpool", "cut", "fly", "strength", "flash", "waterfall"]

# Call helper function to populate dictionary
all_moves = get_moves()

# Define folder name where move data for each move will be stored
folder_name = "move_data"

# Create the folder if it doesn't already exist
os.makedirs(folder_name, exist_ok=True)

# Loop through each move in the dictionary
for move in all_moves:
    # Define file name where data will be stored (name of current move)
    filename =  move + ".txt"

    # Define the file path for the current file (including the folder name)
    file_path = os.path.join(folder_name, filename)

    # Construct the URL that the data will be pulled from
    curr_url = "https://www.serebii.net/attackdex-gs/" + move + ".shtml"

    # Fetch the page, then parse HTML into a variable
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Need to process and distinguish the two "a" tags with the same name, so we get
    # both "a" tags (using findAll to find all instances of the "a" tag "TM")
    # As mentioned above, TM and Special Event tables are both labeled as "TM", hence
    # the need to distinguish. Additionally, HM moves are also labeled as "TM".
    TM_anchors = soup.find_all("a", {"name": "TM"})

    # Declare TM_section as an empty variable so we can check to see if any data was
    # stored in it from the TM data being processed
    TM_section = any
    event_section = any

    # Prepare the text file with informaiton about the current move
    with open(file_path, "w") as file:
        file.write("Pokémon that can learn the move " + all_moves[move])

    # Call helper function to pull the TM_anchors data (this will represent data for
    # both moves learned via level up and moves learned through a special event)
    event_section, TM_section = get_TM_anchors(TM_anchors)

    # Get the levelup data section and the eggmove data section from the parsed HTML
    levelup_section = soup.find("a", {"name": "level"})
    eggmove_section = soup.find("a", {"name": "egg"})

    # First to be processed is learning the move through level up
    # Check to make sure levelup_section contains data before accessing the variable
    if levelup_section:
        # Call helper function to pull data, store results in array
        levelup_data = get_byleveup(levelup_section)
        # Write levelup data to text file
        with open(file_path, "a") as file:
            file.write("\n\nVia Level Up:\n")
            file.write("\n".join(levelup_data))

    # If there is no data in levelup_section, this means no Pokemon can learn the move 
    # via level up. In this case, write "NONE" to that portion of the file
    else:
        with open(file_path, "a") as file:
            file.write("\n\nVia Level Up:\n")
            file.write("NONE")


    # Second to be processed is learning the move through TM/HM
    if TM_section != any:
        # Call helper function to pull data about learning the move through TM/HM
        TM_data = get_byTM(TM_section)

        with open(file_path, "a") as file:
            # If there was TM data found, write it to the file
            if TM_data:
                file.write("\n\nVia TM:\n")
                file.write("\n".join(TM_data)) 
                # This handles the case where the selected move is an HM
                # if(move in HM_moves):
                #     file.write("\n\nVia HM:\n")
                #     file.write("\n".join(TM_data))
                # else:
                #     file.write("\n\nVia TM:\n")
                #     file.write("\n".join(TM_data)) 


    # If there was no data found, write NONE to the file to indicate it        
    else:
        with open(file_path, "a") as file:
            file.write("\n\nVia TM:\n")
            file.write("NONE")    


    # Third to be processed is learning the move through breeding
    # Check and make sure eggmove_section contains data before accessing it
    if eggmove_section:
        # Call helper function to pull data, store results in array
        eggmove_data = get_bybreeding(eggmove_section)
        # Write eggmove data to text file
        with open(file_path, "a") as file:
            file.write("\n\nVia Breeding:\n")
            if eggmove_data:
                file.write("\n".join(eggmove_data))
            else:
                file.write("NONE")

    # If there is no data in eggmove_section, this means no Pokemon can learn the move 
    # via breeding. In this case, write "NONE" to that portion of the file
    else:
        with open(file_path, "a") as file:
            file.write("\n\nVia Breeding:\n")
            file.write("ERROR WITH DATA")


    # Last to be processed is Pokemon that can learn the move through a Special Event
    if event_section != any:
        # Call helper function to pull the data and store in array
        event_data = get_byspecialevent(event_section)

        # After getting all Pokemon names, write them to the text file
        with open(file_path, "a") as file:
            # Make sure event_data contains info to access
            if event_data:
                file.write("\n\nVia Special Event:\n")
                file.write("\n".join(event_data))
    # Handle case where no Pokemon can learn move through a Special Event
    else:
        # Write message to file saying no Pokemon can learn the move via TM
        with open(file_path, "a") as file:
            file.write("\n\nVia Special Event:\n")
            file.write("NONE")

    # Print message confirming data for the current move was processed
    print("Finished processing data for: ", all_moves[move])
