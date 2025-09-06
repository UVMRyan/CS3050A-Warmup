# Author: Ryan Langlois
# This program retrieves data from PokeAPI.co and compiles it into a JSON file.
# I learned how to use PokeAPI from this tutorial: https://youtu.be/JVQNywo4AbU?si=KP08pr2Xi3MvLViS

# Imports
import json
import requests

base_url = "https://pokeapi.co/api/v2/pokemon-species/" # This is where the data is retrieved from.
hyphenated_pokemon = ['ho-oh', 'porygon-z', 'jangmo-o', 'hakamo-o', 'kommo-o']      # These Pokemon have hyphens in their name

# Open the output file
outfile = open('pokemon_data.json', 'w')
outfile.write('[\n')

# Get each Pokemon by their Pokedex number
for pokedex_number in range(1, 1026):

    # Request data for each Pokemon
    url = f"{base_url}{pokedex_number}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:

        print(f"Error: Could not retrieve species data for {pokedex_number}. Status code: {response.status_code}")
        
    else:

        # Convert the response to JSON
        species_data = response.json()

        # Some Pokemon have multiple varieties, so we need to collect data for each one
        for variety in species_data['varieties']:

            # This request is for the specific variety of the Pokemon
            response = requests.get(variety['pokemon']['url'][:-1]) # The URL has a trailing slash that needs to be removed

            if response.status_code != 200:

                print(f"Error: Could not retrieve data for {variety['pokemon']['name']}. Status code: {response.status_code}")
                
            else:

                # The data is initially stored in a dictionary
                dictionary = {}
                pokemon_data = response.json()

                if pokemon_data['name'] in hyphenated_pokemon:

                    dictionary['name'] = pokemon_data['name']

                elif pokemon_data['name'] == 'kommo-o-totem':

                    # This case is special because only one hyphen should be removed
                    dictionary['name'] = 'kommo-o totem'

                else:

                    dictionary['name'] = pokemon_data['name'].replace('-', ' ')

                dictionary['number'] = pokemon_data['id']
                dictionary['height'] = pokemon_data['height']
                dictionary['weight'] = pokemon_data['weight']
                
                # Not every Pokemon evolves from another
                if species_data['evolves_from_species']:

                    if species_data['evolves_from_species']['name'] in hyphenated_pokemon:

                        dictionary['evolves_from'] = species_data['evolves_from_species']['name']

                    else:

                        dictionary['evolves_from'] = species_data['evolves_from_species']['name'].replace('-', ' ')

                dictionary['capture_rate'] = species_data['capture_rate']
                dictionary['gender_ratio'] = species_data['gender_rate']
                dictionary['growth_rate'] = species_data['growth_rate']['name'].replace('-', ' ')
                dictionary['base_experience'] = pokemon_data['base_experience']
                dictionary['legendary'] = species_data['is_legendary']
                dictionary['mythical'] = species_data['is_mythical']
                dictionary['generation'] = species_data['generation']['name'].replace('-', ' ')
                dictionary['type1'] = pokemon_data['types'][0]['type']['name']
                
                # Check if the Pokemon has a second type, some only have one
                if len(pokemon_data['types']) > 1:
                    
                    dictionary['type2'] = pokemon_data['types'][1]['type']['name']
                
                second = False

                # Pokemon can have one or two regular abilities and maybe one hidden ability
                for ability in pokemon_data['abilities']:

                    if ability['is_hidden']:

                        dictionary['hidden_ability'] = ability['ability']['name'].replace('-', ' ')

                    elif second:

                        dictionary['ability2'] = ability['ability']['name'].replace('-', ' ')
                        
                    else:

                        if ability['ability']['name'] == 'well-baked-body':

                            # This case is special because only one hyphen should be removed
                            dictionary['ability1'] = 'well-baked body'

                        else:

                            dictionary['ability1'] = ability['ability']['name'].replace('-', ' ')

                        second = True

                for stat in pokemon_data['stats']:

                    dictionary[stat['stat']['name'].replace('-', ' ')] = stat['base_stat']

                dictionary['egg_group1'] = species_data['egg_groups'][0]['name'].replace('-', ' ')

                # Just like types, some Pokemon have one egg group while others have two
                if len(species_data['egg_groups']) > 1:

                    dictionary['egg_group2'] = species_data['egg_groups'][1]['name'].replace('-', ' ')

                # Convert the dictionary to a string and write it to the output file
                json_string = json.dumps(dictionary, indent=4)

                # If this is the last variety of the last Pokemon, close the JSON array
                if pokedex_number == 1025 and variety == species_data['varieties'][-1]:

                    outfile.write(json_string + ']')

                else:

                    outfile.write(json_string + ',\n')

        # Update the user on progress
        if pokedex_number % 100 == 0:

            print(f"Retrieved data for {pokedex_number} Pokemon.")

outfile.close()