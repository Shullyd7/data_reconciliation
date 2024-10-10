# Data Reconciliation 

This project provides an API for uploading two CSV files and reconciling the data to identify discrepancies.

## Features

- Upload two CSV files (source and target) for reconciliation.
- Normalize data to handle case sensitivity, whitespace, and date formats.
- Identify records present in the source but missing in the target and vice versa.
- Compare records that exist in both files to find discrepancies in specific fields.
- Return reconciliation reports in JSON format.

## Endpoints

### 1. File Upload

- **Endpoint**: `/api/upload/`
- **Method**: `POST`
- **Description**: Accepts two CSV files for reconciliation.
- **Form Data**:
  - `source`: The source CSV file.
  - `target`: The target CSV file.

#### Response

On successful upload:
```json
{
    "message": "Files uploaded and processed successfully."
}
```

### 2. Reconciliation Report

- **Endpoint**: `/api/report/`
- **Method**: `GET`
- **Description**: Returns the reconciliation report based on the uploaded files.
- **Response**:
```json
{
    "missing_in_target": [  ],
    "missing_in_source": [  ],
    "discrepancies": [  ]
}
```

## Installation

### Prerequisites

- Python 3.x
- Django
- Django REST Framework

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shullyd7/data_reconciliation.git
   cd data_reconciliation
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## Testing with Postman

To test the API, import the Postman Collection provided (Assessment.postman_collection.json), or manually create requests.

1. **Upload Files**:
   - Create a `POST` request to `http://localhost:8000/api/upload/`.
   - In the Body tab, select `form-data`, and add the `source` and `target` files.

2. **Get Reconciliation Report**:
   - Create a `GET` request to `http://localhost:8000/api/report/`.

## Atomic Commit Message

- feat: add file upload and reconciliation endpoints