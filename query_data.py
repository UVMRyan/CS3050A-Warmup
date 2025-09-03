from dataclasses import dataclass
import json

list_of_all_pokemon = []
VALID_OPERATORS = ["==", "<", ">", "!="]
VALID_ATTRIBUTES = ["name",###
"number", ###
"height", ###
"weight", ###
"capture_rate",
"gender_ratio",
"growth_rate",
"base_experience",
"legendary",
"mythical",
"generation", ###
"type1", ###
"type2", ###
"ability1",
"hidden_ability",
"hp", ###
"attack", ###
"defense",
"special_attack",
"special_defense",
"speed",
"egg_group1",
"egg_group2"]

@dataclass
class Pokemon:
    name: str ###
    number: int ###
    height: int ###
    weight: int ###
    capture_rate: int
    gender_ratio: int
    growth_rate: str
    base_experience: int
    legendary: bool
    mythical: bool
    generation: str ###
    type1: str ###
    type2: str ###
    ability1: str
    hidden_ability: str
    hp: int ###
    attack: int ###
    defense: int ###
    special_attack: int
    special_defense: int
    speed: int
    egg_group1: str
    egg_group2: str

    # bool
    def comparison(self, compare_field, operator, compare_to):
        if operator == "==":
            return self.__getattribute__(compare_field) == compare_to
        if operator == ">":
            return self.__getattribute__(compare_field) > compare_to
        if operator == "<":
            return self.__getattribute__(compare_field) < compare_to
        if operator == "!=":
            return self.__getattribute__(compare_field) != compare_to


with open('pokemon_data.json', 'r') as f:
    all_pokemon_from_json = json.load(f)
    for pokemon_from_json in all_pokemon_from_json:
        get = pokemon_from_json.get
        new_pokemon = Pokemon(get('name'), get('number'), get('height'), get('weight'), get('capture_rate'), get('gender_ratio'), get('growth_rate'), get('base_experience'), get('legendary'),
              get('mythical'), get('generation'), get('type1'), get('type2'), get('ability1'), get('hidden_ability'), get('hp'), get('attack'), get('defense'),
              get('special_attack'), get('special_defense'), get('speed'), get('egg_group1'), get('egg_group2'))

        list_of_all_pokemon.append(new_pokemon)


print("Enter query (or q to quit): ")


def is_valid_query(query):
    if len(query) != 3:
        return False
    if query[1] not in VALID_OPERATORS:
        return False
    if query[0] not in VALID_ATTRIBUTES:
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
            if pokemon.comparison(split_query[0], split_query[1], int(split_query[2])):
                query_results.append(pokemon)
        for query_result in query_results:
            print(query_result)
    else:
        print("Invalid syntax. Please try again.")
