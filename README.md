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


# Coverage
make sure you installed the requirements.txt file. If not, run the following command :

    pip install coverage

Now run test coverage :

    coverage run manage.py test

to see the results run :

    coverage report


# Code Formatter
Install Black, to follow the project standard format. 

	pip install black 

And run this command before each commit: 
	
	black ./lm
