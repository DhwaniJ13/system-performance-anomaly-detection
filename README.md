# System Performance Anomaly Detection

An end-to-end system performance monitoring and anomaly detection pipeline built with Python, PostgreSQL, PyOD, and Isolation Forest to identify unusual resource-usage patterns.

## Overview

This project monitors system performance metrics, stores the collected data in PostgreSQL, and applies machine learning-based anomaly detection to identify unusual system behavior.

The pipeline combines system monitoring, database storage, data processing, and unsupervised machine learning into a single workflow.

## Problem Statement

System resources such as CPU, memory, disk activity, and network traffic can exhibit unusual patterns that may indicate performance issues or abnormal system behavior.

Manually analyzing these metrics can be difficult when monitoring large numbers of observations.

This project addresses the problem by:

- Collecting system performance metrics
- Persisting monitoring data in PostgreSQL
- Processing the stored data using Python
- Applying Isolation Forest for anomaly detection
- Labeling observations as normal or anomalous

## Architecture

```text
System Metrics
      │
      ▼
Python / psutil
      │
      ▼
PostgreSQL
      │
      ▼
Pandas Data Processing
      │
      ▼
Isolation Forest
      │
      ▼
Anomaly Classification
      │
      ├── Normal
      │
      └── Anomalous