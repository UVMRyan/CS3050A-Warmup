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

int_fields = ['capture rate', 'number', 'special attack', 'defense', 'hp', 'base experience', 'speed', 'height',
              'weight', 'attack', 'special defense']
string_fields = ['name', 'type1', 'type2', 'ability2', 'hidden ability', 'ability1', 'evolves from', 'growth rate',
                 'egg group1', 'egg group2', 'generation']
bool_fields = ['legendary', 'mythical']

# query grammar
operator = oneOf("== != < > of")
compound_operator = oneOf("and or")
field_name = Word(alphanums)
true_keyword = CaselessKeyword("True")
false_keyword = CaselessKeyword("False")
field_value = (pyparsing_common.number |
               Word(alphanums) |
               true_keyword |
               false_keyword)

query_grammar = field_name("field_name1") + \
                operator("operator1") + \
                field_value("field_value1") + \
                Optional(
                    compound_operator("compound_operator") +
                    field_name("field_name2") +
                    operator("operator2") +
                    field_value("field_value2"))


# if the value is a bool, return correct bool, otherwise use the value as it was inputted (string or int)
def normalize_to_bool_or_default(value):
    if value == "true":
        return True
    if value == "false":
        return False
    return value


# parse the query / clean data
def parse_query(query):
    parsed_query_as_dict = query_grammar.parseString(query).asDict()
    get = parsed_query_as_dict.get
    query1 = [get("field_name1"), get("operator1"), normalize_to_bool_or_default(get("field_value1"))]
    if "compound_operator" in parsed_query_as_dict.keys():
        compound = get("compound_operator")
        query2 = [get("field_name2"), get("operator2"), normalize_to_bool_or_default(get("field_value2"))]
        return [query1, compound, query2]
    return [query1]


# runs the raw query
def run_query(query):
    parsed_query = parse_query(query)
    if len(parsed_query) == 1:
        return single_query(parsed_query[0])
    return compound_query(parsed_query[0], parsed_query[1], parsed_query[2])


# returns the result for the query when it is a compound query
def compound_query(query1, compound, query2):
    final_result = []
    field1, op1, value1 = query1
    field2, op2, value2 = query2

    # Input validation
    if op1 == "of" or op2 == "of":
        return ["Error: 'of' operator cannot be used in compound queries"]
    if field1 not in int_fields + string_fields + bool_fields:
        return ["Error: Invalid field name '" + field1 + "'"]
    if field2 not in int_fields + string_fields + bool_fields:
        return ["Error: Invalid field name '" + field2 + "'"]
    if field1 in int_fields and not isinstance(value1, int):
        return ["Error: Field '" + field1 + "' requires an integer value not '" + str(value1) + "'"]
    if field2 in int_fields and not isinstance(value2, int):
        return ["Error: Field '" + field2 + "' requires an integer value not '" + str(value2) + "'"]
    if field1 in bool_fields and not isinstance(value1, bool):
        return ["Error: Field '" + field1 + "' requires a boolean value not '" + str(value1) + "'"]
    if field2 in bool_fields and not isinstance(value2, bool):
        return ["Error: Field '" + field2 + "' requires a boolean value not '" + str(value2) + "'"]

    if compound == "and":
        result_query_1 = db.where(filter=FieldFilter(field1, op1, value1)).stream()
        for doc in result_query_1:
            doc_data = doc.to_dict()
            if op2 == "==":
                if doc_data.get(field2) == value2:
                    final_result.append(doc_data.get("name"))
            if op2 == "!=":
                if doc_data.get(field2) != value2:
                    final_result.append(doc_data.get("name"))
            if op2 == ">":
                if doc_data.get(field2) > value2:
                    final_result.append(doc_data.get("name"))
            if op2 == "<":
                if doc_data.get(field2) < value2:
                    final_result.append(doc_data.get("name"))
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


# returns the result from user query.
def single_query(query):
    result = []
    field, op, value = query

    # input validation different for "of".
    if op == "of":
        # run query to find the pokemon of interest and return the requested field value
        query_result = db.where(filter=FieldFilter("name", "==", str(value))).stream()
        for doc in query_result:
            return [doc.get(field)]
        return ["Error: Name '" + str(value) + "' is not in the dataset"]

    # Input validation
    if field not in int_fields + string_fields + bool_fields:
        return ["Error: Invalid field name '" + field + "'"]
    if field in int_fields and not isinstance(value, int):
        return ["Error: Field '" + field + "' requires an integer value not '" + str(value) + "'"]
    if field in bool_fields and not isinstance(value, bool):
        return ["Error: Field '" + field + "' requires a boolean value not '" + str(value) + "'"]

    # run the query and return the resulting names of pokemon
    query_result = db.where(filter=FieldFilter(field, op, value)).stream()
    for doc in query_result:
        result.append(doc.get("name"))
    return result


# TODO: help menu + initial prompt to user
all_fields = int_fields + string_fields + bool_fields
formatted_fields = ', '.join(f'"{f}"' if ' ' in f else f for f in all_fields)
help_menu = f"""
Help Menu:
- Queries look like: <field> <operator> <value>
- Fields: {formatted_fields}
- Operators: ==, !=, <, >
- Compound queries supported: and, or
- Type q to quit.
"""

print("Enter query, press q to quit, or press help for help: ")
while True:
    query_results = []
    raw_query = input("")
    if raw_query == "help":
        print(help_menu)
        print("Enter query, or press q to quit, or press help for help: ")
        continue
    if raw_query.lower() == "q":
        break

    results = run_query(raw_query)

    if len(results) == 0:
        print("No results found.")
    elif type(results[0]) == int or type(results[0]) == bool or results[0].startswith("Error"):
        print(results[0])
    else:
        print(", ".join(str(r) for r in results))
