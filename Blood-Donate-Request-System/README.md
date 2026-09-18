# Blood Donate & Request System

Django-based CRUD application for donor profiles and blood requests.

## Features
- Registration, login and logout
- User profile update
- Donor profile CRUD
- Blood request CRUD
- Donor search by blood group, location and availability
- Blood request filtering
- Request details and donor details
- Django messages and validation
- Bootstrap responsive UI
- SQLite database

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/
