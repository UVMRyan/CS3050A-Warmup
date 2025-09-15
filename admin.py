# Admin file 
# TODO: Optimize so deletion times are shorter
import json
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Initializing the database and connection to firestore
cred = credentials.Certificate('cs3050-warmup-891d7-firebase-adminsdk-fbsvc-48b3b532ba.json')
firebase_admin.initialize_app(cred)
firestore_conn = firestore.client()

# Read data from the json file
with open('pokemon_data.json', 'r') as pokemonFile:
    pokemonData = json.load(pokemonFile)

# Start new collection in firestore 
collectionReference = firestore_conn.collection("pokemon")

# Check if the collection is populated
docCheck = collectionReference.limit(1).get()

# Docs is every document in the firestore
docs = collectionReference.stream()

# If the collection is populated delete everything
if len(list(docCheck)) >= 1:
    for doc in docs:
        doc.reference.delete()

# Otherwise populate the pokemon collection
for pokemon in pokemonData:
    docID = str(pokemon["number"])
    collectionReference.document(docID).set(pokemon)

