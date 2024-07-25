# README

# Integrated Health Clinic

## About

This combined scheduling and charting web application is a group project for CIS552 Database Design at UMass Dartmouth, Summer 2024. It offers streamlined scheduling, record keeping, and flexibile charting.

## Installation

1. Install PostgreSQL (setup your default user and password)
2. enter `pip install -r requirements.txt`
3. Enter Python shell. Generate django secret key:
  ```python
    from django.core.management.utils import get_random_secret_key
    # copy output
    print(get_random_secret_key())
  ```
4. save DATABASE_PASSWORD and DJANGO_SECRET_KEY as environment variables in your OS
5. In `settings.py`, under `DATABASES` change 'USER' from 'joe' to the username you established in step 2.
6. In your PostgreSQL installation run query `CREATE DATABASE clinic;` as that same user;
7. enter `python manage.py migrate`
8. Run seeds:
  - Seed TimeTable (command in appointments/management/commands): `python manage.py seed_time_table`. 
  - Seed Practitioner: `python manage.py loaddata seed_practitioners.yaml`
9. enter `python manage.py runserver`
10. If you installed pgAdmin4 web, after creating server group, view clinic database at http://127.0.0.1/pgAdmin4

## Features

- Scheduling
- Record Keeping
- Charting

## Schema Database Design

### Entities and Attributes

### Design choices and optimizations

### PostgreSQL and Django ORM