# FindARoomate

This is the back end repository of the FindARoomate.com App. An app that connects students to potential roomates. The repository contains all the APIs used for the app.

## How to use:
*Requirements:*
- Python 3.10 [Ensure to add to path]
- Pipenv. Install with Pip(from Python) with `pip install pipenv`
- Browser. To test the endpoints or use the popular API testers:
  - Curl
  - Postman

*To Begin*
- Clone the repo
- `cd` into the repo
- Run `pipenv shell` to activate the virtual environment
- Run `pipenv install` to install existing dependencies
- create a ".env" file.
- Perform migrations with `python manage.py migrate`
- Create your superuser account with `python manage.py createsuperuser`. Fill in required details.
- To start the server, run `python manage.py runserver`
- start making requests by visiting http://localhost:8000


*Note:*
To install packages, use `pipenv install <package name>`.


