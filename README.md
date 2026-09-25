# Dataset Insights API

A containerized Django REST API that accepts CSV and Excel dataset uploads, performs automated dataset profiling using Pandas, and persists analytical summaries in PostgreSQL.

## 📌 Project Overview

Dataset Insights API is a backend application designed to provide quick insights from uploaded datasets.

The API processes CSV and Excel files and generates useful information about the dataset, including:

- Row and column counts
- Column data types
- Missing value counts
- Duplicate row counts
- Numerical summary statistics

## 🛠️ Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Data Processing:** Pandas, openpyxl
- **Database:** PostgreSQL 16
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git, GitHub

## ✨ Features

- 📁 CSV, XLS and XLSX file upload
- 🔍 Automated dataset profiling
- 📊 Row and column analysis
- 🧩 Column data-type detection
- ⚠️ Missing-value analysis
- ♻️ Duplicate-row detection
- 📈 Numerical summary statistics
- 🗄️ PostgreSQL data persistence
- 🐳 Docker and Docker Compose setup

## 🏗️ Application Flow

```text
Dataset Upload
      ↓
Django REST API
      ↓
Pandas Data Processing
      ↓
Dataset Profiling
      ↓
PostgreSQL
      ↓
Analytical Summary

## API Endpoints

### `POST /api/insights/`

Upload a CSV or Excel file to retrieve dataset profiling metrics.

- **Request Body**: `multipart/form-data`
  - `file`: The `.csv` or `.xlsx` file to process.

- **Success Response (200 OK)**:

```json
{
  "row_count": 100,
  "column_count": 5,
  "columns": ["id", "name", "age", "score", "city"],
  "missing_values": {
    "id": 0,
    "name": 0,
    "age": 2,
    "score": 1,
    "city": 0
  }
}