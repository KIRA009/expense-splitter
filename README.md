# Live Site
- The website is hosted at <a href="https://expensesplitter.pythonanywhere.com/app"> here<a>
- Make an account and add your friends, and manage your expenses

# Local Installation
- Clone the repo in a directory

	`git clone https://github.com/KIRA009/expense-splitter.git`
- Go to the directory

	`cd expense-splitter`
- Create a virtualenv

	`pip install virtualenv`
	`virtualenv .`
- Activate the virtualenv

	`.\Scripts\activate`
- Install all modules and packages

	`pip install -r requirements.txt`
- Go to the django directory

	`cd exp_split`
- make a copy of `config.ini.example` file to `config.ini`

	`copy config.ini.example config.ini`
- Edit the values in the newly created `config.ini` file
- Run the following commands

	```
	manage.py makemigrations
	manage.py migrate
	manage.py runserver
	```
- Go to the <a href="http://127.0.0.1:8000/app/">link</a>