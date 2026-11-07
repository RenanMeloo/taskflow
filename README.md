# TaskFlow API

team task management REST API built with Django REST Framework, featuring JWT authentication and role-based permissions.

## Running locally

1. Clone the repository and create a virtual environment
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set a `SECRET_KEY`
4. `python manage.py migrate`
5. `python manage.py runserver`

API docs: `/api/schema/swagger-ui/`