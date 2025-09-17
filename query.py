# Figuring out a pyparsing grammar just a test file
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from pyparsing import *

VALID_OPERATORS = ["==", "<", ">", "!="]

data = {
    "Name" : "Charizard",
    "number": 6,
    "height": 17,
    "weight": 905,
    "evolves_from": "charmeleon",
    "capture_rate": 45,
    "gender_ratio": 1,
    "growth_rate": "medium slow",
    "base_experience": 240,
    "legendary": False,
    "mythical": False,
    "generation": "generation i",
    "type1": "fire",
    "type2": "flying",
    "ability1": "blaze",
    "hidden_ability": "solar power",
    "hp": 78,
    "attack": 84,
    "defense": 78,
    "special attack": 109,
    "special defense": 85,
    "speed": 100,
    "egg_group1": "monster",
    "egg_group2": "dragon"
}

attribute = Word(alphas, alphanums + "_").setName("attribute")
operator = oneOf(VALID_OPERATORS).setName("operator")
def parse_number(tokens):
    return [int(tokens[0])]

def parse_boolean(tokens):
    return [tokens[0] == "True"]

number = Word(nums).setParseAction(parse_number)
boolean = oneOf("True False").setParseAction(parse_boolean)
string_value = Word(alphas).setName("string_value")

value = number | boolean | string_value

expr = attribute + operator + value

