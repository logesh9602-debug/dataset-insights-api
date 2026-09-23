# Dataset Insights API

A containerized Django REST API that accepts CSV and Excel dataset uploads, performs automated profiling using Pandas, and persists analytical summaries in PostgreSQL.

## Tech Stack
- **Backend:** Django 5.x, Django REST Framework
- **Data Processing:** Pandas, openpyxl
- **Database:** PostgreSQL 16
- **Containerization:** Docker & Docker Compose

## Features
- File upload handling (`.csv`, `.xls`, `.xlsx`).
- Automated calculation of row/column count, column data types, missing value counts, duplicate rows, and numerical summary statistics.
- Data persistence in PostgreSQL via Docker named volumes (`pgdata`).

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/logesh9602-debug/dataset-insights-api.git
   cd dataset-insights-api