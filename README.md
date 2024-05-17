# Djote
backend note project with django


# Setup locally
- Make a copy of Djote/local_settings_sample.txt file in project root directory and rename it to local_settings.py
- Update new file with your local database credentials 
- Run `pip install -r requirements.txt`
- Create a database with local_settings credentials
- Run `python manage.py migrate`
- Run `python manage.py runserver`

visit `http://127.0.0.1:8000/`


# Test


to run test the project entirely:

     python manage.py test

to test only one app:

    python manage.py test app_name 


# Code Formatter
Install Black, to follow the project standard format. 

	pip install black 

And run this command before each commit: 
	
	black ./lm

# Docker Settings

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

Make Sure you have the local_setting file on the main root directory of your project with your credentials and the Host value is db:
    
    "HOST": "db"

Now you can build the Docker images and start the containers:

    docker-compose up --build

Apply the Django migrations:
 
    docker-compose exec web python manage.py migrate

Create a superuser
    
    docker-compose exec web python manage.py createsuperuser

Your Django project is now up on docker 

# Docker Commands

Building the Docker Images

    docker-compose build

Starting the Containers

    docker-compose up

Stopping the Containers

    docker-compose down