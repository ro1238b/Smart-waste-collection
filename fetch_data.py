import firebase_admin
from firebase_admin import credentials, firestore

# Load your service account key
cred = credentials.Certificate("D:\wastemanagement\waste-6fd9a-firebase-adminsdk-fbsvc-02b41bb60d.json")

# Initialize app only once
firebase_admin.initialize_app(cred)

# Now create Firestore client
db = firestore.client()


docs= db.collection("readings").stream()

latest={}


for doc in docs:
    data=doc.to_dict()
    bin_id=data["bin_id"]

    ts=datetime.datetime.fromisoformat(data["timestamp"])

    if bin_id not in latest or ts > latest[bin_id]["timestamp"]:
        latest[bin_id]={
            "bin_id":bin_id,
            "fill_level_percent":data["fill_level_percent"],
            "timestamp":ts,
            "location":data.get("loaction")
        }

all_bins=list(latest.values())

print("Total unique bins",len(all_bins))
print("Example",all_bins[:3])