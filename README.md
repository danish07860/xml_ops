# 🚀 XML Ops Data Pipeline (PySpark + Airflow)

An end-to-end **data engineering pipeline** that ingests encrypted XML data, performs validation, and delivers clean, structured outputs with automated scheduling and alerting.

---

## 🧠 Overview

This project simulates a **real-world ETL pipeline**:

Encrypted XML → Decryption → Spark Processing → DQ Checks → Output → Email → Airflow Scheduling

---

## ⚙️ Tech Stack

- **Processing:** PySpark  
- **Orchestration:** Apache Airflow  
- **Language:** Python  
- **Data Format:** XML  
- **Security:** GPG Encryption  
- **Notifications:** SMTP (Email)  
- **Logging:** Python Logging  
- **Config:** JSON (DQ rules), `.env`

---

## 🔐 Key Features

### 1. Encrypted Data Ingestion
- Handles `.gpg` encrypted XML files
- Decrypts using passphrase (non-interactive)

### 2. XML Processing with PySpark
- Uses `spark-xml` package  
- Supports schema enforcement  
- Handles nested XML structures  

### 3. Data Quality (DQ) Engine
- Config-driven rules (`dq_rules.json`)
- Supports:
  - Null checks  
  - Format validation  
  - Range validation  
- Multi-error detection per row  
- Single-pass optimized aggregation  

### 4. Data Segregation
- Splits:
  - ✅ Valid records  
  - ❌ Invalid records (with error reasons)

### 5. Output Generation
- Clean XML output  
- Bad records XML  
- JSON DQ report  

### 6. Email Notification System
- Sends DQ report via SMTP  
- HTML + plain text email  
- Includes formatted table + signature  

### 7. Logging & Monitoring
- Centralized logging  
- File + console logs  
- Error trace with stack info  

### 8. Fault Tolerance
- Retry mechanism for:
  - Decryption  
  - Email sending  
- Failure alerts via email  

### 9. Workflow Orchestration (Airflow)
- DAG-based scheduling  
- Runs via `spark-submit`  
- Retry + monitoring via UI  

---

## 📂 Project Structure

xml_ops/
├── dags/
│   └── xml_pipeline_dag.py
├── jobs/
│   └── xml_pipeline.py
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── utils/
├── config/
│   └── dq_rules.json
├── data/
├── logs/
├── .env
├── README.md

---

## 🚀 How to Run

### 1. Setup Environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Set Environment Variables

INPUT_PATH=data/raw/customers.xml.gpg  
GPG_PASSPHRASE=your_passphrase  
EMAIL_SENDER=your_email@gmail.com  
EMAIL_PASSWORD=app_password  
EMAIL_RECEIVER=receiver_email@gmail.com  

### 3. Run Pipeline (Manual)

spark-submit --packages com.databricks:spark-xml_2.12:0.17.0 jobs/xml_pipeline.py

### 4. Run via Airflow

airflow standalone  
Open UI → http://localhost:8080  

---

## 🧑‍💻 Author

Danish Shaikh  
GitHub: https://github.com/danish07860/xml_ops
