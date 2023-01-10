# Introduction

The goal of this project is creation simple blog site.
Project is writen with django3, python3.11, poetry.

*place for photo*

### Main features

# Getting Started

1. Clone this reprository.
```
$ git clone <reference>
```

2. Activate virtual enviroment
```
$ poetry shell
```

3. Install project dependencies
```
$ poetry install   
```

4. Make migrations
```
$ cd siteblog
$ python manage.py makemigrations
$ python manage.py migrate
```

# Usage

1. Create file *setenv.sh* in the project root and write variables by this template:
	```
	export SECRET_KEY='<your secret key>'
	export SMTP_EMAIL='<your smtp email>'
	export TEST_EMAIL_FOR_RECEIVING_EMAIL='<your test email for receiving>'
	```

2. Export variables in your enviroment
```
$ . ../setenv.sh
```

2. You can now run the development server:
```
$ python manage.py runserver
```
