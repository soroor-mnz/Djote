# Djote
backend note project by django


# Setup locally
- Make a copy of Djote/local_settings_sample.txt file in project root directory and rename it to local_settings.py
- Update new file with your local database credentials 
- Run `pip install -r requirements.txt`
- Create a database with local_settings credentials
- Run `python manage.py migrate`
- Run `python manage.py runserver`


# Code Documentation
you can visit 

    http://127.0.0.1:8000/

to get a full version documented api UI view generated by Swagger.

you can also check out 
    
    http://127.0.0.1:8000/schema/

to download a yml file version of the API documents. and 

    http://127.0.0.1:8000/schema/redoc/

for sample versioned UI.




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
