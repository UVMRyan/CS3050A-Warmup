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

int_fields = ['capture rate', 'number', 'special attack', 'defense', 'hp', 'base experience', 'speed', 'height', 'weight', 'attack', 'special defense']
string_fields = ['name', 'type1', 'type2', 'ability2', 'hidden ability', 'ability1', 'evolves from', 'growth rate', 'egg group1', 'egg group2', 'generation']
bool_fields = ['legendary', 'mythical']

# query grammar
operator = oneOf("== != < > of")
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

    # Input validation
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
    if op1 == "of" or op2 == "of":
        return ["Error: 'of' operator cannot be used in compound queries"]

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


def single_query(query):
    result = []
    field, op, value = query

    # Input validation
    if field not in int_fields + string_fields + bool_fields:
        return ["Error: Invalid field name '" + field + "'"]
    if field in int_fields and not isinstance(value, int):
        return ["Error: Field '" + field + "' requires an integer value not '" + str(value) + "'"]
    if field in bool_fields and not isinstance(value, bool):
        return ["Error: Field '" + field + "' requires a boolean value not '" + str(value) + "'"]

    if op == "of":
        query_result = db.where(filter=FieldFilter("name", "==", value)).stream()
        for doc in query_result:
            return doc.get(field)

    query_result = db.where(filter=FieldFilter(field, op, value)).stream()
    for doc in query_result:
        result.append(doc.get("name"))
    return result

# 
print("Enter query, or press q to quit: ")
while True:
    query_results = []
    raw_query = input(">>> ").lstrip('>').strip()
    if raw_query == "q" or raw_query == "Q":
        break

    results = run_query(raw_query)

    if len(results) == 0:
        print("No results found.")
    elif results[0].startswith("Error"):
        print(results[0])
    else:
        print(", ".join(str(r) for r in results))

    print("Enter query, or press q to quit: ")
