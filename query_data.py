from dataclasses import dataclass
import json
from pyparsing import *

VALID_OPERATORS = ["==", "<", ">", "!="]
ATTRIBUTES = {"name": str,
              "number": int,
              "type1": str,
              "type2": str,
              "evolves_from": str,
              "legendary": bool,
              "mythical": bool,
              "ability1": str,
              "ability2": str,
              "hidden_ability": str,
              "hp": int,
              "attack": int,
              "defense": int,
              "special_attack": int,
              "special_defense": int,
              "speed": int
              }


@dataclass
class Pokemon:
    name: str
    number: int
    type1: str
    type2: str
    evolves_from: str
    legendary: bool
    mythical: bool
    ability1: str
    ability2: str
    hidden_ability: str
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    # bool
    def comparison(self, compare_field, operator, compare_to):
        compare_to = ATTRIBUTES[compare_field](compare_to)
        if operator == "==":
            return self.__getattribute__(compare_field) == compare_to
        if operator == ">":
            return self.__getattribute__(compare_field) > compare_to
        if operator == "<":
            return self.__getattribute__(compare_field) < compare_to
        if operator == "!=":
            return self.__getattribute__(compare_field) != compare_to


list_of_all_pokemon = []
with open('pokemon_data.json', 'r') as f:
    all_pokemon_from_json = json.load(f)
    for pokemon_from_json in all_pokemon_from_json:
        get = pokemon_from_json.get
        new_pokemon = Pokemon(get('name'), get('number'), get('type1'), get('type2'), get('evolves_from'),
                              get('legendary'), get('mythical'),
                              get('ability1'), get('ability2'), get('hidden_ability'), get('hp'), get('attack'),
                              get('defense'),
                              get('special_attack'), get('special_defense'), get('speed'))
        list_of_all_pokemon.append(new_pokemon)

print("Enter query (or q to quit): ")

def is_valid_query(query):
    if len(query) != 3:
        return False
    if query[1] not in VALID_OPERATORS:
        return False
    if query[0] not in ATTRIBUTES.keys():
        return False
    return True

while True:
    query_results = []
    raw_query = input("")
    if raw_query == "q":
        break
    split_query = raw_query.split(' ')
    if is_valid_query(split_query):
        for pokemon in list_of_all_pokemon:
            if pokemon.comparison(split_query[0], split_query[1], split_query[2]):
                query_results.append(pokemon.name)
        for query_result in query_results:
            print(query_result)
    else:
        print("Invalid syntax. Please try again.")

# Create a grammar using pyparser
