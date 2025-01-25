# CRM Dashboard - Django Project
#### Overview

This Django project uses PostgreSQL as the database. It provides an API to list users and includes a custom management command to populate the database with random data.
## Prerequisites

Ensure you have the following installed:

    Python 3.x
    PostgreSQL


## Steps to Set Up ~
## 1. Install Python Dependencies

Create a virtual environment and install the required Python packages.

#### Create a virtual environment
> python3 -m venv env

#### Activate the virtual environment
##### On Windows:
> env\Scripts\activate
##### On Mac/Linux:
> source env/bin/activate

#### Install dependencies
> pip install -r requirements.txt

## 2. Set Up PostgreSQL Database

#### Create Database:

    # Log in to PostgreSQL
    psql -U postgres
    
    # Create a new database
    CREATE DATABASE crm_dashboard;

### Configure PostgreSQL: Update your DB related information in `.env` file. This details will be used in `settings.py`:
    SECRET_KEY=Your_Project_Secret_Key
    DB_NAME=crm_dashboard
    DB_USER=postgres # replace with your PostgreSQL username
    DB_PASSWORD=password # replace with your PostgreSQL username
    DB_HOST=localhost
    DB_PORT=5432

## 3. Run Migrations

Apply the migrations to set up the database schema.

##### Run migrations
> python manage.py migrate

## 4. Populate the Database with Random Data

Use the custom management command to populate the database with sample data.

##### Populate the database with random data. Creates 3 million records in your DB
> python manage.py populate_data

## 5. Start the Django Development Server

Run the server to start the API.

##### Start the Django development server
> python manage.py runserver

## 6. Access the API

To list users with sorting and filtering, access the following API:

`http://localhost:8000/api/users?sort=-points&range=0-1000&first_name=Zoe`

    sort: Sorting by the field (e.g., -points for descending order). [Sort is applicable for all the parameters]
    range: Pagination range (e.g., 0-1000 for the first 1000 records).
    first_name: Filter by the user's first name (e.g., Zoe). [Filter is applicable for all the parameters]

### Notes:

    Ensure your PostgreSQL server is running locally.
    If you encounter errors during the populate_data command, check your PostgreSQL connection and database credentials.
