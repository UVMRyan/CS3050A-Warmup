# Admin file 
import json
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Initializing the database and connection to firestore
cred = credentials.Certificate('cs3050-warmup-891d7-firebase-adminsdk-fbsvc-48b3b532ba.json')
firebase_admin.initialize_app(cred)

# Create connection to the firestore
firestore_conn = firestore.client()

with open('pokemon_data.json', 'r') as pokemonFile:
    pokemonData = json.load(pokemonFile)

collectionReference = firestore_conn.collection("pokemon")

for pokemon in pokemonData:
    docID = str(pokemon["number"])
    collectionReference.document(docID).set(pokemon)

