# System Performance Anomaly Detection

> An end-to-end machine learning pipeline for monitoring system performance, storing telemetry data in PostgreSQL, and detecting unusual resource-usage patterns using Isolation Forest.

## Overview

System performance can fluctuate due to changes in CPU utilization, memory usage, disk activity, and network traffic.

This project collects system performance metrics, stores the collected data in PostgreSQL, retrieves and processes the data using Python, and applies unsupervised anomaly detection to identify observations that differ from normal system behavior.

The project demonstrates an end-to-end data science workflow:

**System Monitoring → Database Storage → Data Processing → Anomaly Detection → Results**

---

## Key Results

| Metric | Result |
|---|---:|
| Records processed | 54 |
| Normal observations | 48 |
| Detected anomalies | 6 |
| Anomaly rate | 11.1% |

> Results shown above are from the current local test dataset.

---

## Project Architecture

```mermaid
flowchart LR
    A[System Performance Metrics] --> B[Python + psutil]
    B --> C[PostgreSQL]
    C --> D[Pandas Data Processing]
    D --> E[Feature Preparation]
    E --> F[Isolation Forest]
    F --> G[Anomaly Classification]
    G --> H[Normal / Anomalous Records]