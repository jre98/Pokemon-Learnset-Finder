import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import re

# Helper functions that process each possible way a Pokemon can learn a move (via:
# Level Up, TM/HM, Breeding/Egg Moves, and Special Events)

# TODO
# Write helper function for TM data extraction (equivalent to "if TM_anchors" in main file)
def get_TM_anchors(TM_anchors):
    print()


# Pulls the data about which Pokemon can learn the move via Level Up and returns a 
# list of the names of those Pokemon
def get_byleveup(levelup_section):
    # Find the table right after the "level" anchor
    table = levelup_section.find_next("table", class_="dextable")

    # Pull the data from each row in the table except the first two. The first row
    # contains header info such as Pokedex #, Pokemon Name, Base Stats, level the 
    # Pokemon learns the move at, etc. while the second row contains subheadings 
    # for the Base Stats (HP, Attack, etc.) and for the level the Pokemon learns 
    # the move at (Gold/Silver vs. Crystal) 
    levelup_rows = table.find_all("tr")[2:] 
  
    # Container to store the results
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

    # Return the data that was extracted
    return levelup_data

# Pulls the data about which Pokemon can learn the move via TM/HM and returns a 
# list of the names of those Pokemon (this works for HMs as well as TMs due to the)
# way the anchor tags are labeled in the HTML
def get_byTM(TM_section):
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
    
    # Return the extracted data
    return TM_data

# Pulls the data about which Pokemon can learn the move through Breeding (Egg Moves)
def get_bybreeding(eggmove_section):
    # Find the table right after the "egg" anchor
    table = eggmove_section.find_next("table", class_="dextable")

     # Pull the data from each row in the table (skip the first two header rows)
    eggmove_rows = table.find_all("tr")[2:]

    # Container to store results
    eggmove_data = []

    # Examine each row from the list of rows
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
  
    # Return the extracted data
    return eggmove_data

# Pulls the data about which Pokemon can learn the move through a Special Event
def get_byspecialevent(event_section):
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

    # Return the extracted data
    return event_data
