import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

# -----------------------------
# Initialize Firestore
# -----------------------------
cred = credentials.Certificate('D:\wastemanagement\waste-6fd9a-firebase-adminsdk-fbsvc-02b41bb60d.json')  # Path to your Firebase service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

# -----------------------------
# 1️⃣ Fetch overflowing bins
# -----------------------------
overflow_query = db.collection("readings").where("fill_level_percent", "<", 90)
overflow_bins = overflow_query.stream()

print("Bins currently overflowing:")
for doc in overflow_bins:
    data = doc.to_dict()
    print(f"{data['bin_id']} at {data['timestamp']} - Fill: {data['fill_level_percent']}%")

# -----------------------------
# 2️⃣ Fetch all readings for a specific bin
# -----------------------------
bin_id = "BIN042"
bin_readings_query = db.collection("readings").where("bin_id", "==", bin_id)
bin_readings_docs = bin_readings_query.stream()

bin_readings_list = []
for doc in bin_readings_docs:
    bin_readings_list.append(doc.to_dict())

# Convert to DataFrame for analysis
bin_df = pd.DataFrame(bin_readings_list)
print(f"\nAll readings for {bin_id}:")
print(bin_df.head())

# -----------------------------
# 3️⃣ Aggregate by day/week
# -----------------------------
# Convert timestamp to datetime
bin_df['timestamp'] = pd.to_datetime(bin_df['timestamp'])

# Aggregate daily
daily_agg = bin_df.groupby(bin_df['timestamp'].dt.date)['fill_level_percent'].mean().reset_index()
daily_agg.rename(columns={'fill_level_percent': 'avg_fill_level_percent'}, inplace=True)
print("\nDaily average fill level:")
print(daily_agg)

# Aggregate weekly
weekly_agg = bin_df.groupby(bin_df['timestamp'].dt.isocalendar().week)['fill_level_percent'].mean().reset_index()
weekly_agg.rename(columns={'fill_level_percent': 'avg_fill_level_percent'}, inplace=True)
print("\nWeekly average fill level:")
print(weekly_agg)
