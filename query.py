# Figuring out a pyparsing grammar just a test file

# to suppress the warnings from firebase
import os

os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_ENABLE_STDERR_LOG"] = "0"

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from google.cloud.firestore import FieldFilter
from pyparsing import *

# make the firebase connection
cred = credentials.Certificate('cs3050-warmup-891d7-firebase-adminsdk-fbsvc-48b3b532ba.json')
firebase_admin.initialize_app(cred)
firestore_conn = firestore.client()
db = firestore_conn.collection("pokemon")

data = {
    "Name": "Charizard",
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

# query grammar
operator = oneOf("== != < >")
compound_operator = oneOf("and or")
field_name = Word(alphanums)
field_value = (pyparsing_common.number | Word(alphanums))

query_grammar = field_name("field_name1") + \
                operator("operator1") + \
                field_value("field_value1") + \
                Optional(
                    compound_operator("compound_operator") +
                    field_name("field_name2") +
                    operator("operator2") +
                    field_value("field_value2"))


def parse_query(query):
    parsed_query_as_dict = query_grammar.parseString(query).asDict()
    get = parsed_query_as_dict.get
    query1 = [get("field_name1"), get("operator1"), get("field_value1")]
    if "compound_operator" in parsed_query_as_dict.keys():
        compound = get("compound_operator")
        query2 = [get("field_name2"), get("operator2"), get("field_value2")]
        return [query1, compound, query2]
    return [query1]


def run_query(query):
    parsed_query = parse_query(query)
    if len(parsed_query) == 1:
        return single_query(parsed_query[0])
    return compound_query(parsed_query[0], parsed_query[1], parsed_query[2])


def compound_query(query1, compound, query2):
    final_result = []
    field1, op1, value1 = query1
    field2, op2, value2 = query2
    if compound == "and":
        result_query_1 = db.where(filter=FieldFilter(field1, op1, value1)).stream()
        for doc in result_query_1:
            doc_data = doc.to_dict()
            if op2 == "==":
                if doc_data.get(field2) == value2:
                    final_result.append(data)
            if op2 == "!=":
                if doc_data.get(field2) != value2:
                    final_result.append(data)
            if op2 == ">":
                if doc_data.get(field2) > value2:
                    final_result.append(data)
            if op2 == "<":
                if doc_data.get(field2) < value2:
                    final_result.append(data)
    if compound == "or":
        result_query_1 = single_query(query1)
        result_query_2 = single_query(query2)
        for element in result_query_1:
            if element not in final_result:
                final_result.append(element)
        for element in result_query_2:
            if element not in final_result:
                final_result.append(element)
    return final_result


def single_query(query):
    result = []
    field, op, value = query
    query_result = db.where(filter=FieldFilter(field, op, value)).stream()
    for doc in query_result:
        result.append(doc.get("name"))
    return result


print("enter query, or press q to quit: ")
while True:
    query_results = []
    raw_query = input("")
    if raw_query == "q":
        break
    print(run_query(raw_query))
