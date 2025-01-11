# This file is used to get a list of each possible Gen II move. The list can then be
# used to loop through each move from Gen II to extract the data about it

import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import json

# Store in a function so it can be called from the main file
def get_moves():
    # Choosing the webpage of a random attack, as each attack webpage contains the same
    # list of moves in a <SELECT> div, which we will extract from
    curr_url = "https://www.serebii.net/attackdex-gs/ember.shtml"

    # Fetch the page, then parse HTML into a variable
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <select> tags (the dropdown lists containing each move from Gen II are 
    # <SELECT> divs with the name "SelectURL"). Since there are three of these, we 
    # need to store them in a list to deal with each one individually
    select_tags = soup.find_all("select", {"name": "SelectURL"})

    # Dictionary that will store each move (using a dictionary becuase two-word moves 
    # are formatted without spaces in the url - "Fire Blast" is "fireblast.shtml"). 
    # Used to put the correct text in the URL and also in the text document the data is
    # saved to. Key is unformatted text, value is formatted text.
    move_dict = {}

    # Loop through each <SELECT> tag, as the lists are stored in three different
    # dropdown lists.
    for tag in select_tags:
        # For the current select tag, iterate through all <option> tags it contains
        for option in tag.find_all("option"):
            # Get the value attribute for the current option
            value = option.get("value")
            # Make sure value contains data before accessing it
            if value:
                # Extract the unformatted name (i.e., "fireblast") from the option. This
                # would be the text after the second '/' and before '.shtml'
                key = value.split("/")[-1].split(".")[0]

                # Next, extract the text that is displayed in the dropdown (this is the
                # correctly ormatted name, i.e., "Fire Blast")
                display_text = option.get_text(strip=True)

                # Store in dictionary, with unformatted as key and formatted as value
                move_dict[key] = display_text

    # Now that dictionary is populated, return it
    return move_dict


# This part of the code creates a json file with the list of all moves (this is used
# by the Javascript function for autocomplete/typeahead)

all_moves = get_moves()
# Extract only the formatted move names (values)
moves_list = list(all_moves.values())

# Path to save the JSON file

json_file_path = "/Users/jacob/Desktop/Pokemon-Learnset-Finder/webapp/movelist.json"

# Writing the moves list to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(moves_list, json_file, indent=4)

print(f"Movelist saved to {json_file_path}")



