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
fetch("move_data.json")
    .then(response => response.json())
    .then(data =>{
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
    // Prevent form from reloading page upon submission
    event.preventDefault(); // Prevent the form from reloading the page
  
    const move1 = document.getElementById("move1").value;
    const move2 = document.getElementById("move2").value;
    const move3 = document.getElementById("move3").value;
    const move4 = document.getElementById("move4").value;
  
    const moves = [move1, move2, move3, move4].filter(Boolean); // Remove empty inputs
  
    if (moves.length === 0) {
      alert("Please enter at least one move.");
      return;
    }

    // console.log(move1)
  
    // Find Pokémon that can learn the moves
    const results = findCommonPokemon(moves);
  
    // Display the results
    const resultsDiv = document.getElementById("results");
    if (results.length > 0) {
      resultsDiv.innerHTML = results
        .map(
          (pokemon) =>
            `<p>${pokemon.name}: ${pokemon.methods
              .map(
                (method) => `<strong>${method.type}</strong>: ${method.details.join(", ")}`
              )
              .join(" | ")}</p>`
        )
        .join("");
    } else {
      resultsDiv.innerHTML = "No Pokémon found that can learn all the selected moves.";
    }
  });



  // Function to find Pokémon that can learn the given moves
function findCommonPokemon(moves) {
    const pokemonMap = new Map();
  
    // Loop through each move from the moves array (which stores the moves the user inputted)
    moves.forEach((move) => {
      // Retrieve the data for the current move from the json file
      const moveInfo = move_data[move];
      // Skip if move is not found in JSON
      if (!moveInfo) return; 

      // Create array of key-value pairs for the move data. "method" stores the way in which
      // the move is learned (Level Up, TM, Breeding, Special Event). "mons" store a list of
      // Pokemon (in the case of TM or breeding) or a nested object (for level up)
      Object.entries(moveInfo).forEach(([method, mons]) => {

        // Next, need to handle the different learning methods. First, TMs and breeding
        if (Array.isArray(mons)) {
          // Handle breeding and TM cases
          mons.forEach((pokemon) => {
            if (!pokemonMap.has(pokemon)) {
              pokemonMap.set(pokemon, []);
            }
            pokemonMap.get(pokemon).push({ type: method, details: [] });
          });
        } else {
          // Handle level-up cases, which is a nested object, as we have the Pokemon name as
          // well as the level they learn the move at
          Object.entries(mons).forEach(([pokemon, details]) => {
            if (!pokemonMap.has(pokemon)) {
              pokemonMap.set(pokemon, []);
            }
            pokemonMap.get(pokemon).push({ type: method, details });
          });
        }
      });
    });
  
    // Find Pokémon that appear in all move lists
    return Array.from(pokemonMap.entries())
      .filter(([_, methods]) => methods.length === moves.length)
      .map(([name, methods]) => ({ name, methods }));
  }
// Function to search for Pokemon that can learn the inputted set of moves
