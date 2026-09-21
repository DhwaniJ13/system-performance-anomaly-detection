import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy import create_engine
from pyod.models.iforest import IForest

# Connecting to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Reading data from PostgreSQL
data = pd.read_sql("SELECT * FROM system_performance", engine)
print("Rows fetched from DB:", len(data))

# Selecting feature columns
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

# Creating PyOD model - Isolation Forest
model = IForest(
    contamination=0.1,
    random_state=42
)

# Converting features to NumPy array
X_values = features.values

# Training the model
model.fit(X_values)

# Predicting anomalies
data["anomaly"] = model.predict(X_values)

# Result:
# 0 = normal
# 1 = anomaly

# Viewing detected anomalies
print("\nDetected Anomalies:")
print(data[data["anomaly"] == 1])

print("\nFull Data:")
print(data)

print("\nAnomaly column values:")
print(data["anomaly"].value_counts())