# User Behavior Analytics Platform (PySpark)

## 📌 Overview

This project implements a distributed data processing pipeline using PySpark to analyze user behavior data at scale. It simulates a real-world data engineering workflow, including ETL processing, sessionization, and analytical data modeling.

The pipeline processes raw event logs and produces curated analytics datasets that support user engagement analysis and content performance tracking.

---

## 🏗️ Architecture

The pipeline follows a layered data architecture commonly used in modern data platforms:

Bronze (Raw Data) → Silver (Cleaned & Enriched Data) → Gold (Analytics Tables)

This design ensures data quality, reusability, and scalability.

---

## ⚙️ Tech Stack

- **PySpark** (distributed data processing)
- **Parquet** (columnar storage format)
- **SQL / DataFrame API**
- **Window Functions**
- **Git-based project structure**

---

## 🔄 Data Pipeline (ETL)

### Extract
- Ingest raw user events, user profiles, and content metadata from Parquet sources

### Transform
- Clean and validate event data
- Enrich events via joins with dimension tables
- Implement sessionization using window functions (lag, cumulative aggregation)

### Load
- Store processed datasets into structured analytics tables (Gold layer)

---

## 📊 Data Modeling (Analytics Layer)

The pipeline produces the following analytical datasets:

### User Metrics
- Daily Active Users (DAU)
- Events per user
- User engagement metrics

### Session Metrics
- Session duration
- Event count per session

### Content Analytics
- Top N content per category using ranking functions (`row_number`)

---

## ⚡ Performance Optimization

The pipeline incorporates several distributed data processing optimizations:

### 1. Broadcast Join
- Small dimension tables are broadcasted to reduce shuffle cost

### 2. Data Skew Handling
- Skewed keys are mitigated using salting techniques to balance workload across partitions

### 3. Partition Management
- Repartitioning is applied to improve parallelism
- Output partitions are controlled using `repartition` to prevent small file issues

### 4. Shuffle Optimization
- Aggregations leverage map-side combine to reduce shuffle volume

---

## 📂 Project Structure
analytics_spark_project/
├── jobs/ # Pipeline entry point
├── pipeline/ # Pipeline orchestration
├── transformations/ # Core business logic
├── utils/ # Spark session & IO utilities
├── data/ # Bronze / Silver / Gold layers


---

## ▶️ How to Run

```bash
python jobs/run_pipeline.py
💡 Key Engineering Concepts

Distributed data processing with Spark

ETL pipeline design

Data partitioning and shuffle optimization

Window functions for sessionization and ranking

Handling data skew in large-scale datasets

🚀 Potential Improvements

Integrate workflow orchestration (e.g., Airflow)

Deploy on cloud platforms (AWS EMR / Databricks)