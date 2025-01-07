import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import re

# Import helper functions
from extract_helper_funcs import *

# Import function that will get the list of all moves from Gen II
from get_gen2_movelist import get_moves



# Dictionary containing all moves from the Gen II Pokemon Games
all_moves = {}

# Call helper function to populate dictionary
all_moves = get_moves()




# Current move that is having data pulled
curr_move = "ember"
# URL to pull info from
curr_url = "https://www.serebii.net/attackdex-gs/" + curr_move +".shtml"

# Fetch the page, then parse HTML into a variable
response = requests.get(curr_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Need to process and distinguish the two "a" tags with the same name, so we get
# both "a" tags (using findAll to find all instances of the "a" tag "TM")
# As mentioned above, TM and Special Event tables are both labeled as "TM", hence
# the need to distinguish. Additionally, HM moves are also labeled as "TM"
TM_anchors = soup.find_all("a", {"name": "TM"})

# List containing the HM moves that have the possiblity to come up. In these
# cases, we want to change what is written to the text file for the title for
# TM vs HM, as they are labeled the same in the HTML
HM_moves = ["surf", "whirlpool", "cut", "fly", "strength", "flash", "waterfall"]

# Prepare the text file with informaiton about the current move
# Write levelup data to text file
with open("level_up_info.txt", "w") as file:
    file.write("Pokémon that can learn the move " + curr_move)

# Declare TM_section as an empty variable so we can check to see if any data was
# stored in it from the TM data being processed
TM_section = any
event_section = any


# First, check to see if the TM_anchors variable contains any data to process.
# This will be the case when the move can be learned via TM or HM
if TM_anchors:
# If there is data, loop through each table associated with the "a" tag with name "TM"
    for anchor in TM_anchors:
        # Get the text immediately after the anchor (to see which table we are dealing with)
        text_after_anchor = anchor.find_next(string=True).strip()
        # print("The current text after the anchor is: ", text_after_anchor)

        # First check is to see if the text "Event or a special way" occurs in the text after
        # the anchor. This indicates that this is the table representing Pokemon who learn the
        # move through an event or in some other special way
        if "Event or a special way" in text_after_anchor:
            # Confirm that we are processing the event/special way table
            print("Processing the Event table...")
            # Store the table after the text we found in a new variable (this will store only
            # info about Pokemon who learn the move through a special event or some other way)
            event_section = anchor.find_next("table", class_="dextable")
            
        # This checks to make sure we are accessing the correct data for the Pokemon that can
        # learn the move through TM

        elif "TM" in text_after_anchor:
            # Confirm that we are processing
            print("Processing the TM table...")
            TM_section = anchor.find_next("table", class_="dextable")
            # print(tm_table)

        # Handle errors
        else:
            print("TM_anchors were found, but was unable to find specified text after anchors")
# Do nothing if there is no TM or Special Event data to pull
else:
    print("No TM anchors found")

# Pokemon that learn the move by level up
levelup_section = soup.find("a", {"name": "level"})

# Pokemon that learn the move through breeding (i.e., egg moves)
eggmove_section = soup.find("a", {"name": "egg"})

# First to be processed is learning the move through level up
# Check to make sure levelup_section contains data before accessing the variable
if levelup_section:
    # Call helper function to pull data, store results in array
    levelup_data = get_byleveup(levelup_section)
    # Write levelup data to text file
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Level Up:\n")
        file.write("\n".join(levelup_data))

# If there is no data in levelup_section, this means no Pokemon can learn the move 
# via level up. In this case, write "NONE" to that portion of the file
else:
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Level Up:\n")
        file.write("NONE")

# Second to be processed is learning the move through TM/HM
if TM_section != any:
    # Call helper function to pull data about learning the move through TM/HM
    TM_data = get_byTM(TM_section)

    with open("level_up_info.txt", "a") as file:
        # If there was TM data found, write it to the file
        if TM_data:
            # This handles the case where the selected move is an HM
            if(curr_move in HM_moves):
                file.write("\n\nVia HM:\n")
                file.write("\n".join(TM_data))
            else:
                file.write("\n\nVia TM:\n")
                file.write("\n".join(TM_data)) 

# If there was no data found, write NONE to the file to indicate it        
else:
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia TM:\n")
        file.write("NONE")    


# Third to be processed is learning the move through breeding
# Check and make sure eggmove_section contains data before accessing it
if eggmove_section:
    # Call helper function to pull data, store results in array
    eggmove_data = get_bybreeding(eggmove_section)
    # Write eggmove data to text file
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Breeding:\n")
        if eggmove_data:
            file.write("\n".join(eggmove_data))
        else:
            file.write("NONE")

# If there is no data in eggmove_section, this means no Pokemon can learn the move 
# via breeding. In this case, write "NONE" to that portion of the file
else:
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Breeding:\n")
        file.write("ERROR WITH DATA")

# Last to be processed is Pokemon that can learn the move through a Special Event
if event_section != any:
    # Call helper function to pull the data and store in array
    event_data = get_byspecialevent(event_section)

    # After getting all Pokemon names, write them to the text file
    with open("level_up_info.txt", "a") as file:
        # Make sure event_data contains info to access
        if event_data:
            file.write("\n\nVia Special Event:\n")
            file.write("\n".join(event_data))
# Handle case where no Pokemon can learn move through a Special Event
else:
    # Write message to file saying no Pokemon can learn the move via TM
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Special Event:\n")
        file.write("NONE")