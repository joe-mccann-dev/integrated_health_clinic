# README

# Integrated Health Clinic

## About

This combined scheduling and charting web application is a group project for CIS552 Database Design at UMass Dartmouth, Summer 2024. It offers streamlined scheduling, record keeping, and flexibile charting.

## Installation

1. Install Python
2. Install PostgreSQL (setup your default user and password)
3. Install Django using pip (https://docs.djangoproject.com/en/5.0/topics/install/#installing-official-release)
4. Install psycopg (https://www.psycopg.org/psycopg3/docs/basic/install.html)
5. Generate django secret key:
  ```python
    from django.core.management.utils import get_random_secret_key
    # copy output
    print(get_random_secret_key())
  ```
6. save DATABASE_PASSWORD and DJANGO_SECRET_KEY as environment variables in your OS
7. In `settings.py`, under `DATABASES` change 'USER' from 'joe' to the username you established in step 2. Change `TIME_ZONE` from 'UTC' to 'America/New_York'
8. In your PostgreSQL installation run query `CREATE DATABASE clinic` as that same user;
9. run `python manage.py migrate`
10. run `python manage.py runserver`

## Features

- Scheduling
- Record Keeping
- Charting

## Schema Database Design

### Entities and Attributes

### Design choices and optimizations

### PostgreSQL and Django ORM