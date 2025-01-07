# Always want to get to the section in the HTML that says: "Pokémon that learn 'Move#X'
# by Level up". This is directly before the table for the levels for Gold/Silver and
# Crystal. For learning the move by breeding, find the point in the HTML that says: 
# "Pokémon that learn 'Move#X by Breeding".

# Upon inspection, it was found that both the TM table and the Move Through a Special
# Event Table use "a" tags with the name "TM." The beginning of this code processes the
# two tables and splits them into their appropriate sections.
# Additionally, HM moves (such as Surf, Cut, Whirpool, etc.) are labeled in the HTMl
# with the "a" tag with name "TM", just as with the actual TMs. This makes things easier 
# in handling those cases, as all that needs to be done is check for the HM moves before
# writing to the text file.

import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import re

from extract_move import *

# Current move that is having data pulled
curr_move = "barrier"
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

# Do nothing if there is no TM or Special Event data to process
else:
    print("No TM anchors found")

# Pokemon that learn the move by level up
levelup_section = soup.find("a", {"name": "level"})

# Pokemon that learn the move through TM are stored in "TM_section"
# Pokemon that learn the move through a special event/other way are stored in "event_section"

# Pokemon that learn the move through breeding (i.e., egg moves)
eggmove_section = soup.find("a", {"name": "egg"})



# First, process the data in "levelup_section" to extract the Pokemon names and the level
# they learn the move at.
# Making sure level_section has data before trying to access it
if levelup_section:
    # Find the table right after the "level" anchor
    table = levelup_section.find_next("table", class_="dextable")

    # Pull the data from each row in the table (need to skip first two header rows, 
    # explanation below)
    levelup_rows = table.find_all("tr")[2:] 
    # First row contains header info such as Pokedex #, Pokemon name, type, base 
    # stats, level the pokemon learns the move, etc. 
    # Second row contains subheadings for the Base Stats (HP, Attack, etc.) and 
    # for the Level Learned (Gold/Silver vs. Crystal levels).

    # Container to store results
    levelup_data = []

    # Examine each individual row from the list of rows
    for row in levelup_rows:
        # print("The current row in LEVEUP is:\n", row, "\n")
        # Get the data for each column in the current row
        cols = row.find_all("td", class_="fooinfo")
        # Make sure there are enough columns so that the correct data is extacted
        if len(cols) > 11:
            # Need to extract the 3rd column for the Pokemon's name and also the 11th 
            # and 12th columns for the Levels the move is leared at in G/S vs. C  
            pokemon_name = cols[2].get_text(strip=True)

            # Level move is learned at in Gold/Silver
            level_GS = cols[10].get_text(strip=True)
            # Level move is learned at in Crystal
            level_C = cols[11].get_text(strip=True)

            # If multiple levels are listed, split them and reformat (correct split location found
            # using a regular expression)
            level_GS_formatted = ", ".join(re.findall(r'Lv\.\s?\d+', level_GS))
            # level_C_formatted = ", ".join([f"{level}" for level in level_C.split(", ")])
            level_C_formatted = ", ".join(re.findall(r'Lv\.\s?\d+', level_C))

            # Format the final data result for the current Pokemon
            formatted_entry = f"{pokemon_name}: {level_GS_formatted} | {level_C_formatted}"

            # Add the relevant info to the results array
            levelup_data.append(formatted_entry)

   
    # Write levelup data to text file
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Level Up:\n")
        file.write("\n".join(levelup_data))
       

    print("Level-up information extracted and saved to level_up_info.txt")
# Handle error or case where the levelup table could not be found
else:
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Level Up:\n")
        file.write("NONE")

# Second, process the data in "TM_section" to extract the Pokemon names
# Make sure TM_section contains data before trying to access it
if TM_section != any:
    # Pull the data from each row in the table (skip the first two header rows)
    TM_rows = TM_section.find_all("tr")[2:]

    # Container to store results
    TM_data = []

    # Examine each individual row from the list of rows
    for row in TM_rows:
        # Get the data for each column in the current row
        cols = row.find_all("td", class_="fooinfo")

        # Skips rows that contain undeeded data (only need Mon names)
        if len(cols) > 9:
            # Extract the 3rd column containing the Pokemon's name
            pokemon_name = cols[2].get_text(strip=True)

            # print("The current Pokemon is: ", pokemon_name)

            # Add the name to the results array
            TM_data.append(pokemon_name)

    # After getting all Pokemon names, write them to the text file
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
# Handle error or case where TM or HM table could not be found    
else:
    # Write message to file saying no Pokemon can learn the move via TM
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia TM:\n")
        file.write("NONE")
    print("error with TM data")

# Third, process the data in "eggmove_section" to extract the Pokemon names (need to 
# extract more information about the egg moves later from a separate source).
# Make sure eggmove_section has data before trying to access it
if eggmove_section:
    # Find the table right after the "egg" anchor
    table = eggmove_section.find_next("table", class_="dextable")

    # Pull the data from each row in the table (skip the first two header rows)
    eggmove_rows = table.find_all("tr")[2:]

    # Container to store results
    eggmove_data = []

    # Examine each individual row from the list of rows
    for row in eggmove_rows:
        # Get the data for each column in the current row
        cols = row.find_all("td", class_="fooinfo")
        
        # Skip rows that don't contain valid data (e.g., rows with Pokémon names)
        if len(cols) > 9:  
            # Extract the 3rd column for the Pokémon's name
            pokemon_name = cols[2].get_text(strip=True)

            # Print the current Pokémon name (optional, for debugging purposes)
            # print("The current Pokemon is: ", pokemon_name)

            # Add the Pokémon name to the results array
            eggmove_data.append(pokemon_name)    
  
    # Write eggmove data to text file
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Breeding:\n")
        if eggmove_data:
            file.write("\n".join(eggmove_data))
        else:
            file.write("NONE")

    # Print message confirming data was saved to the text file
    print("Egg Move information extracted and saved to level_up_info.txt")
# Handle errors or case where no Pokemon can learn the move via breeding
else:
    print("error with egg moves")

if event_section != any:
    # Pull the data from each row in the table (skip first two header rows)
    event_rows = event_section.find_all("tr")[2:]

    # Container to store results
    event_data = []

    # Examine each individual row from the list of rows
    for row in event_rows:
        # Get the data for each column in the current row
        cols = row.find_all("td", class_="fooinfo")

         # Skips rows that contain undeeded data (only need Mon names)
        if len(cols) > 9:
            # Extract the 3rd column containing the Pokemon's name
            pokemon_name = cols[2].get_text(strip=True)

            # Add the name to the results array
            event_data.append(pokemon_name)

    # After getting all Pokemon names, write them to the text file
    with open("level_up_info.txt", "a") as file:
        # Make sure event_data contains info to access
        if event_data:
            file.write("\n\nVia Special Event:\n")
            file.write("\n".join(event_data))
# Handle case where no event info was found for the move
else:
    # Write message to file saying no Pokemon can learn the move via TM
    with open("level_up_info.txt", "a") as file:
        file.write("\n\nVia Special Event:\n")
        file.write("NONE")
    # print("error with TM data")



