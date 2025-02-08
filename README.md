# BullRun backend
Official Backend of BullRun

How to run locally

1.  Setup and activate virtual environment within root directory
-----
#For Mac
- python -m venv venv
- source venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt

#For windows 
- python -m venv venv
- venv/Scripts/activate
- pip install --upgrade pip
- pip install -r requirements.txt

2. Set up local database
------
- python manage.py makemigrations
- python manage.py migrate 

3. Run the server
- python manage.py runserver
