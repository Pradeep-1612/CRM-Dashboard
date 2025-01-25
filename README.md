# CRM Dashboard - Django Project
#### Overview

This Django project uses PostgreSQL as the database. It provides an API to list users and includes a custom management command to populate the database with data.
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

#### Configure PostgreSQL: Update your DB related information in `.env` file. This details will be used in `settings.py`:
    SECRET_KEY=Your_Project_Secret_Key
    DB_NAME=crm_dashboard
    DB_USER=postgres # replace with your PostgreSQL username
    DB_PASSWORD=password # replace with your PostgreSQL username
    DB_HOST=localhost
    DB_PORT=5432

## 3. Run Migrations

Apply the migrations to set up the database schema.

##### Make migrations in your local setup
> python manage.py makemigrations

##### Run migrations
> python manage.py migrate

## 4. Populate the Database with Data ~  3 million records

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

Sort and Filter applies for all the parameters.

    sort: Sorting by the field (e.g., -points for descending order).
    range: Pagination range (e.g., 0-1000 for the first 1000 records).
    first_name: Filter by the user's first name (e.g., Zoe).

### Notes:

    Ensure your PostgreSQL server is running locally.
    If you encounter errors during the populate_data command, check your PostgreSQL connection and database credentials.
## :star2: Query Performance and Optimization Analysis

##### :white_check_mark: [Analysis 1] Indexing `first_name` and `points`:
Took **617ms**, indicating that indexing in this case didn’t significantly optimize performance.

<img height="300" width="500" alt="Screenshot 2025-01-25 at 4 31 32 PM" src="https://github.com/user-attachments/assets/9f87cbdf-50ed-4080-9a2c-e44d98e77b20" />

##### :white_check_mark: :white_check_mark: [Analysis 2] Querying `AppUser -> Address, CustomerRelationship` without indexes:
Took **217ms**, suggesting this approach is already fairly optimized without indexes.

<img height="300" width="500" alt="Screenshot 2025-01-25 at 5 06 11 PM" src="https://github.com/user-attachments/assets/1f2b20c0-e68f-4c23-8c4d-b8e9ad668bef" />

##### :white_check_mark: :white_check_mark: :white_check_mark: [Analysis 3] Querying `CustomerRelationship -> AppUser -> Address` without indexes:
Fastest at **115ms**, showing that sequential scans work better than indexing for this specific query.

<img height="300" width="500" alt="Screenshot 2025-01-25 at 5 18 14 PM" src="https://github.com/user-attachments/assets/db8bd083-9a91-4bed-8d3f-7d463f86246e" />



