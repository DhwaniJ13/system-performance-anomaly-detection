import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd      #for handling table
from sqlalchemy import create_engine      #read data from PostgreSQL
from pyod.models.iforest import IForest      #Pyod algorithm used-Isolation Forest model

#connecting to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

#to read data from PostgreSQL
data = pd.read_sql("SELECT * FROM system_performance", engine)
print("Rows fetched from DB:", len(data))

#selecting feature colns
features = data[[
    "cpu_usage_percent",
    "gpu_usage_percent",
    "memory_usage_percent",
    "available_ram_mb",
    "disk_read_mbps",
    "disk_write_mbps",
    "network_sent_kbps",
    "network_received_kbps"
]]

#creating PyOD model-Isolation Forest
model = IForest(contamination=0.1, random_state=42) 
#asssuming 10% of data may be anomaly
#random state to make results reproducible

#training above used model 
model.fit(features)

#predicting anomalies
data["anomaly"] = model.predict(features)
#result-> 0- data is normal
#         1- anomaly

#viewing detected anomalies- prints only abnormal system states
print("\nDetected Anomalies:")
print(data[data["anomaly"] == 1])

print("\nFull Data:")
print(data)

print("\nAnomaly column values:")
print(data["anomaly"].value_counts())
