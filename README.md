
# Rhombus Assessment Backend (rhombus-assessment-be)

This project is a Django-based backend application for handling CSV file uploads, viewing data with inferred column types, and tracking upload history. It includes endpoints for managing and updating column types inferred from CSV files.

## Prerequisites

Ensure the following packages are installed in your environment:

- `dateparser` - For parsing date values from CSV files
- `django` - The primary web framework used
- `django-cors-headers` - For handling Cross-Origin Resource Sharing (CORS)

Install these dependencies using pip:

```bash
pip install dateparser django django-cors-headers
```

## Setup and Installation

### Clone the repository

```bash
git clone https://github.com/phuoc-nh/rhombus-assessment-be
cd rhombus-assessment-be
```

### Set up the database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser for admin access
```bash
python manage.py createsuperuser
```

### Run the development server
```bash
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/


## API Endpoints

POST `/api/upload/`
**Description**: Upload a CSV file.

Sample request:
```json
{
	"file": "sample_data.csv"
}
```

GET `/api/upload/`
**Description**: Retrieve paginated data from an uploaded file along with inferred column types. This step will infer the column types if they have not been set manually. 

-  Parameters
   - `page` (optional): The page number to retrieve (default: 1)
   - `limit` (optional) - Number of entries per page.
   - `file_id` (required) - The ID of the uploaded file.

Sample request:
```
/api/upload/?file_id=26&limit=20&page=1
```

Sample response:

```json
{
    "file_id": 26,
    "data": "[{\"transaction_id\": 101, \"customer_name\": \"Alice Wonderland\", \"purchase_amount\": 123.45, \"purchase_date\": \"2022-01-15T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"10\", \"city\": \"San... Diego\", \"verified\": true}, {\"transaction_id\": 102, \"customer_name\": \"Bob Builder\", \"purchase_amount\": 200.0, \"purchase_date\": \"2022-01-22T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"5\", \"city\": \"New York\", \"verified\": false}, {\"transaction_id\": 103, \"customer_name\": \"Charlie Brown\", \"purchase_amount\": 450.0, \"purchase_date\": \"2024-03-05T00:00:00\", \"product_code\": \"2021-11-11T00:00:00\", \"discount\": \"20\", \"city\": \"Los Angeles\", \"verified\": true}, {\"transaction_id\": 104, \"customer_name\": \"Dora Explorer\", \"purchase_amount\": \"NaN\", \"purchase_date\": \"2021-11-10T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"NaN\", \"city\": \"Tokyo\", \"verified\": false}, {\"transaction_id\": 105, \"customer_name\": \"Eric Cartman\", \"purchase_amount\": 1000.0, \"purchase_date\": \"2023-02-18T00:00:00\", \"product_code\": \"2024-08-11T00:00:00\", \"discount\": \"5\", \"city\": \"Chicago\", \"verified\": false}, {\"transaction_id\": 106, \"customer_name\": \"Fiona Shrek\", \"purchase_amount\": \"NaN\", \"purchase_date\": \"2022-03-20T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"NaN\", \"city\": \"New Delhi\", \"verified\": true}, {\"transaction_id\": 107, \"customer_name\": \"George Jetson\", \"purchase_amount\": 150.0, \"purchase_date\": \"2021-04-10T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"15\", \"city\": \"Paris\", \"verified\": true}, {\"transaction_id\": 108, \"customer_name\": \"Harry Potter\", \"purchase_amount\": 275.5, \"purchase_date\": \"2022-05-11T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"NaN\", \"city\": \"London\", \"verified\": true}, {\"transaction_id\": 109, \"customer_name\": \"Indiana Jones\", \"purchase_amount\": \"NaN\", \"purchase_date\": \"2024-07-01T00:00:00\", \"product_code\": \"2023-11-11T00:00:00\", \"discount\": \"NaN\", \"city\": \"Berlin\", \"verified\": false}, {\"transaction_id\": 110, \"customer_name\": \"Jack Sparrow\", \"purchase_amount\": 800.0, \"purchase_date\": \"2021-08-30T00:00:00\", \"product_code\": \"NaT\", \"discount\": \"10\", \"city\": \"Miami\", \"verified\": true}]",
    "types": {
        "customer_name": "text",
        "purchase_amount": "number",
        "purchase_date": "dateTime",
        "product_code": "dateTime",
        "discount": "text",
        "city": "text",
        "verified": "boolean"
    },
    "total_pages": 1
}
```

GET `/api/files`
**Description**: Retrieve a list of all uploaded files for history tracking.

Sample response:
```json
[
    {
        "id": 1,
        "file": "sample_data_ICsYTIP.csv"
    },
    {
        "id": 2,
        "file": "sample_data_Pde3vNs.csv"
    }
]
```

PUT `/api/upload/`
**Description**: Update the inferred column types for a previously uploaded file.

Sample request:
```json
{
	"file_id": 1,
    "types": {
        "Name": "text",
        "Birthdate": "dateTime",
        "Score": "number",
        "Grade": "category",
        "Boolean": "boolean"
    }
}
```
