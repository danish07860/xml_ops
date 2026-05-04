# 🚀 XML Ops Data Pipeline

An end-to-end **production-style data pipeline** built using PySpark that ingests encrypted XML data, applies schema validation and data quality checks, and generates outputs with automated email reporting.

---

## 🧠 Overview

This project demonstrates how to design and implement a **real-world data engineering pipeline** with multiple layers:

* 🔐 Secure ingestion using GPG encryption/decryption
* ⚡ Distributed processing using PySpark
* 📊 Schema enforcement and validation
* 🧪 Data Quality (DQ) checks
* 🔀 Good/Bad data segregation
* 📁 Structured output (XML + JSON)
* 📧 Automated email reporting

---

## 🏗️ Architecture

```text
Encrypted XML (.gpg)
        ↓
GPG Decryption
        ↓
XML File
        ↓
PySpark Ingestion
        ↓
Schema Enforcement
        ↓
Data Quality Layer
        ↓
Data Segregation
   ├── Good Records
   └── Bad Records
        ↓
Output Layer
   ├── XML (good/bad)
   └── JSON (DQ report)
        ↓
Email Notification (SMTP)
```

---

## ⚙️ Tech Stack

* **Python 3**
* **PySpark**
* **GPG (Encryption/Decryption)**
* **SMTP (Email Notification)**
* **Spark XML Package**
* **dotenv (Config Management)**

---

## 📂 Project Structure

```text
xml_ops/
│
├── src/
│   ├── ingestion/
│   │   ├── load_xml.py
│   │   └── decrypt_gpg.py
│   │
│   ├── processing/
│   │   └── dq_checks.py
│   │
│   ├── utils/
│   │   ├── config_loader.py
│   │   └── email_utils.py
│
├── jobs/
│   └── xml_pipeline.py
│
├── data/
│   ├── raw/
│   ├── output/
│
├── .env
├── .gitignore
└── README.md
```

---

## 🔐 Key Features

### ✔ Secure Data Ingestion

* Supports `.gpg` encrypted files
* Non-interactive decryption using passphrase

---

### ✔ Schema Enforcement

* Explicit schema applied using Spark
* Avoids incorrect data inference

---

### ✔ Data Quality Framework

Rules implemented:

| Rule            | Condition     |
| --------------- | ------------- |
| NULL_ID         | id is NULL    |
| NULL_EMAIL      | email is NULL |
| INVALID_EMAIL   | missing '@'   |
| NEGATIVE_INCOME | income < 0    |

Each record includes:

* `error_reason`
* `is_valid` flag

---

### ✔ Data Segregation

* ✅ **Good Data** → Valid records
* ❌ **Bad Data** → Invalid records with error reason

---

### ✔ Output Layer

| Output       | Format | Path                         |
| ------------ | ------ | ---------------------------- |
| Good Records | XML    | `data/output/good_xml/`      |
| Bad Records  | XML    | `data/output/bad_xml/`       |
| DQ Report    | JSON   | `data/output/dq_report.json` |

---

### ✔ Email Notification

* Sends DQ report after pipeline execution
* Subject format:

```text
DQ Report - YYYY-MM-DD
```

* Uses secure **App Password (SMTP)** authentication

---

## 🚀 How to Run

### 1️⃣ Set environment variables

Create `.env`:

```env
INPUT_GPG=data/raw/customers_100.xml.gpg
GPG_PASSPHRASE=your_passphrase

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver@gmail.com
```

---

### 2️⃣ Activate environment

```bash
source venv/bin/activate
```

---

### 3️⃣ Run pipeline

```bash
export PYTHONPATH=$(pwd)

spark-submit \
  --packages com.databricks:spark-xml_2.12:0.17.0 \
  jobs/xml_pipeline.py
```

---

## 📧 Email Setup (Important)

* Enable **2-Step Verification**
* Generate **App Password**
* Use it in `.env` (not your real password)


---

## 💯 What This Project Demonstrates

* End-to-end pipeline design
* Data validation strategies
* Secure data handling
* Modular architecture
* Real-world engineering practices

---

## 👨‍💻 Author

Danish

---

## ⭐ If you found this useful

Give it a ⭐ on GitHub!
