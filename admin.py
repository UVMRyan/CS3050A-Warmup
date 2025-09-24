# Admin file 
import json
import sys
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Check the length of command-line input, if length != print help statement
if len(sys.argv) != 2:
    print("Input: admin.py pokemon_data.json")
    sys.exit(1)

# Get the filename
json_file = sys.argv[1]

# Initialize Firestore connection
cred = credentials.Certificate('cs3050-warmup-891d7-firebase-adminsdk-fbsvc-48b3b532ba.json')
firebase_admin.initialize_app(cred)
firestore_conn = firestore.client()

# Read data from the given JSON file
with open(json_file, 'r') as f:
    pokemon_data = json.load(f)

# Initialize collection
collection_name = "pokemon"
collection_ref = firestore_conn.collection(collection_name)

# Check if the collection is populated
doc_check = collection_ref.limit(1).get()
docs = collection_ref.stream()

# If the collection contains documents delete all
if len(list(doc_check)) >= 1:
    print("Deleting all documents in the collection...")
    for doc in docs:
        doc.reference.delete()
print("All documents deleted from the firestore.")

# Once deletion from collection is complete upload documents into collection
print("Adding pokemon to the firestore...")
for pokemon in pokemon_data:
    doc_ID = str(pokemon["number"])
    if doc_ID:
        collection_ref.document(doc_ID).set(pokemon)
    else:
        collection_ref.add(pokemon)
print(f"Upload Complete.")