import psutil
import pandas as pd
import time

# 🔹 step 2 + step 3 imports
from sqlalchemy import create_engine
from pyod.models.iforest import IForest


# 🔹 connect python to PostgreSQL database
engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/system_monitoring"
)


# 🔁 AUTOMATION LOOP (runs continuously)
while True:

    print("\nCollecting system data...")

    # creating table with parameters observed
    cols = [
        "cpu_usage_percent",
        "gpu_usage_percent",
        "memory_usage_percent",
        "available_ram_mb",
        "disk_read_mbps",
        "disk_write_mbps",
        "network_sent_kbps",
        "network_received_kbps"
    ]

    data = pd.DataFrame(columns=cols)

    # collecting cpu usage
    cpu = psutil.cpu_percent(interval=1)

    # collecting memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    available_ram = memory.available / (1024 * 1024)

    # collecting disk read/write
    disk1 = psutil.disk_io_counters()
    time.sleep(1)
    disk2 = psutil.disk_io_counters()

    disk_read = (disk2.read_bytes - disk1.read_bytes) / (1024 * 1024)
    disk_write = (disk2.write_bytes - disk1.write_bytes) / (1024 * 1024)

    # collecting network usage
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()

    net_sent = (net2.bytes_sent - net1.bytes_sent) / 1024
    net_recv = (net2.bytes_recv - net1.bytes_recv) / 1024

    # gpu not available → set 0
    gpu_usage = 0

    # creating row of collected data
    new_row = {
        "cpu_usage_percent": cpu,
        "gpu_usage_percent": gpu_usage,
        "memory_usage_percent": memory_usage,
        "available_ram_mb": available_ram,
        "disk_read_mbps": disk_read,
        "disk_write_mbps": disk_write,
        "network_sent_kbps": net_sent,
        "network_received_kbps": net_recv
    }

    # adding row into dataframe
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    print(data)

    # 🔹 inserting into PostgreSQL
    data.to_sql(
        name="system_performance",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data inserted into PostgreSQL")


    # 🔥 STEP-3: ANOMALY DETECTION

    # reading only recent data (SCALING)
    data_db = pd.read_sql("""
        SELECT * FROM system_performance
        ORDER BY id DESC
        LIMIT 500
    """, engine)

    # check minimum data
    if len(data_db) >= 10:

        features = data_db[[
            "cpu_usage_percent",
            "gpu_usage_percent",
            "memory_usage_percent",
            "available_ram_mb",
            "disk_read_mbps",
            "disk_write_mbps",
            "network_sent_kbps",
            "network_received_kbps"
        ]]

        # creating model
        model = IForest(contamination=0.1, random_state=42)

        # training + predicting
        data_db["anomaly"] = model.fit_predict(features)

        anomalies = data_db[data_db["anomaly"] == 1]

        if len(anomalies) > 0:
            print("\n🚨 ANOMALIES DETECTED:")
            print(anomalies)
        else:
            print("\n✅ No anomalies detected")

    else:
        print("Not enough data for anomaly detection")

    print("\nWaiting for next cycle...\n")

    # 🔹 change interval here
    time.sleep(10)   # use 10 sec for testing, later change to 60