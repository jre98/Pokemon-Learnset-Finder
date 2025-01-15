// List to store all moves so they can be accessed for typeahead
let move_list = [];

// List to store data about each move (which Pokemon can learn the move and by which method)
let move_data;

// Pull the move names from the .json file containing all move names
fetch("movelist.json")
    .then(response => response.json())
    .then(data => {
        // Store in the list for access
        move_list = data;
    })
    // Catch errors when pulling .json file
    .catch(error => console.error("Error loading move names:", error));

// Pull the move data from the other json file
fetch("movedata_namesonly.json")
    .then(response => response.json()).then(data => {
        move_data = data
    })
    // Catch error when pulling from .json file
    .catch(error => console.error("Error loading move data:", error));

// Function for autocomplete/typeahead in move input fields
document.addEventListener("DOMContentLoaded", () => {
    // Select all input fields with the 'move-input' class - these represent each input field for moves
    // Allows for iteration through each "move-input" element
    const moveInputs = document.querySelectorAll(".move-input");

    // Loop through each input field
    moveInputs.forEach(inputField => {
        // Select the <div> immediately following the current inputField (the div following the inputField will
        // always be the suggestions div)
        const suggestionsBox = inputField.nextElementSibling;

        // Listen for user input of typing in the text box, triggers function when user types in box
        inputField.addEventListener("input", () => {
            // Retrieve the current value on the input field. Remove leading and trailing white spaces and also
            // convert to lower case for case-insensitive input matching
            const query = inputField.value.toLowerCase().trim();
            // Clear previous suggestions from the suggestionsBox div
            suggestionsBox.innerHTML = "";

            // Stop and exit function if input is empty - no need to suggest inputs if the user hasn't typed
            // anything yet
            if (query === "") {
                return;
            }

            // Filter moves based on the input query. Convert to lowercase again for case-insensitive
            // input matching
            const filteredMoves = move_list.filter(move =>
                move.toLowerCase().startsWith(query)
            );

            // Display matching suggestions (loop through each matching suggestion)
            filteredMoves.forEach(move => {
                // Create a new div to store the suggestions
                const suggestionItem = document.createElement("div");
                suggestionItem.className = "suggestion-item";
                // Set the text in the div to the current move
                suggestionItem.textContent = move;

                // Add click event to select the move so that if the user clicks on one of the 
                // suggestions, their selection will fill the text box
                suggestionItem.addEventListener("click", () => {
                    inputField.value = move;
                    // If the user selects a move from the list, clear the suggestions dropdown
                    suggestionsBox.innerHTML = "";
                });

                // Once the suggestionItem <div> is complete, add it to the suggestionsBox so that
                // the suggestions are displayed
                suggestionsBox.appendChild(suggestionItem);
            });
        });

        // If the user clicks outside the suggestions box, hide it (typical behavior)
        document.addEventListener("click", (event) => {
            // Do not hide if the user clicks inside the suggestions box or inside the input box
            if (!suggestionsBox.contains(event.target) && event.target !== inputField) {
                suggestionsBox.innerHTML = ""; // Clear suggestions
            }
        });
    });
});



// Function to handle the form submission
document.getElementById("move-form").addEventListener("submit", (event) => {
    // Prevent form from reloading the page upon submission
    event.preventDefault();

    // Store each inputted move in a variable
    const move1 = document.getElementById("move1").value;
    const move2 = document.getElementById("move2").value;
    const move3 = document.getElementById("move3").value;
    const move4 = document.getElementById("move4").value;

    // Put moves in array and remove any empty inputs with .filter(Boolean)
    const moves = [move1, move2, move3, move4].filter(Boolean); 

    // If the length of the moves array is 0, then this means the user did not enter 
    // a move. In this case, prompt them to enter at least one move
    if (moves.length === 0) {
        alert("Please enter at least one move.");
        return;
    }

    // Find Pokémon that can learn the moves using helper function
    const results = findCommonPokemon(moves);

    // Display the results by creating a new <div>
    const resultsDiv = document.getElementById("results");
    if (results.length > 0) {
        resultsDiv.innerHTML = results
            .map((pokemon) => `<p>${pokemon}</p>`)
            .join("");
    } else {
        resultsDiv.innerHTML = "No Pokémon found that can learn all the selected moves.";
    }
});

// Function that will find the common Pokemon across all the moves enetered by the user
function findCommonPokemon(moves) {
    // Use a map to track Pokémon counts across all selected moves
    const pokemonCountMap = new Map();

    // Loop through each move in the moves array
    moves.forEach((move) => {
        // Get the list of Pokemon that can learn the current move
        const pokemonList = move_data[move]; 
        // Handle errors where a move was not found
        if (!pokemonList) {
            console.warn(`Move "${move}" not found in data.`);
            return;
        }

        // Then, for each Pokemon that was found, add it to the Map structure
        pokemonList.forEach((pokemon) => {
            // If the Pokemon name was not yet in the map, add it and set the count to 0
            if (!pokemonCountMap.has(pokemon)) {
                pokemonCountMap.set(pokemon, 0);
            }
            // If the Pokemon name is already in the Map, increment the count for that Pokemon
            pokemonCountMap.set(pokemon, pokemonCountMap.get(pokemon) + 1);
        });
    });

    // Filter Pokémon that appear for all selected moves (stored in an array for testing validation)
    let found_mons = Array.from(pokemonCountMap.entries())
        // This portion filters out results where the "count" for a Pokemon in the map is not equal to
        // the length of the "moves" array. That is, only include in the results Pokemon that can
        // learn the moves inputted by the user
        .filter(([_, count]) => count === moves.length)
        // Extract only the Pokemon names
        .map(([name]) => name);

    // Return the filtered array so we can use it to display the results
    return found_mons;

}


