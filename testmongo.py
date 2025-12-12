import pandas as pd
from pymongo import MongoClient , UpdateOne

client=MongoClient("mongodb://localhost:27017/")

db=client["smart_waste_db"]

bins_col=db["bins"]
recordings_col=db["recordings"]

df=pd.read_csv(r"D:\wastemanagement\notebook\waste_bin_data3.csv")


def parse_location(loc_str):
    s= str(loc_str).replace("(","").replace(")","").replace(" ","")
    lat, lon =s.split(",")
    return float(lat),float(lon)


print("inserting into bins")


bins_df =df[['bin_id','location','area_type']].drop_duplicates()
bin_ops=[]

for _, row in bins_df.iterrows():
    lat, lon =parse_location(row['location'])

    bin_ops.append(
        UpdateOne(
            {"bin_id":row["bin_id"]},
            {
                "$set":{
                    "bin_id":row["bin_id"],
                    "location_lat":lat,
                    "location_lon":lon,
                    "location":{"lat":lat,"lon":lon},
                    "area_type":row["area_type"]
                }
            }, 
            upsert=True
        )
    )

if bin_ops:
    bins_col.bulk_write(bin_ops)

print("bins inserted",len(bin_ops))


print("Inserting into recordings...")

records = []

for _, r in df.iterrows():
    lat, lon = parse_location(r["location"])

    rec = {
        "bin_id": r["bin_id"],
        "timestamp": pd.to_datetime(r["timestamp"]),
        "fill_level_percent": float(r["fill_level_percent"]),
        "waste_type": r.get("waste_type"),
        "temperature_celsius": float(r["temperature_celsius"]),
        "humidity_percent": float(r["humidity_percent"]),
        "rainfall_mm": float(r["rainfall_mm"]),
        "holiday_flag": int(r["holiday_flag"]),
        "weekend_flag": int(r["weekend_flag"]),
        "sensor_error_flag": int(r["sensor_error_flag"]),
        "overflow_label": int(r["overflow_label"]),
        "location_lat": lat,
        "location_lon": lon  # helpful for faster analytics
    }

    records.append(rec)

# Insert all rows
recordings_col.insert_many(records)

print("✔ Recordings inserted:", len(records))
print("🎉 All 36,000 rows uploaded successfully!")