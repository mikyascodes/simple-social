# simple-social
This project is about the basics of a social network application. The users can create an account-> complete their profile-> then they can follow other users.  Also they can send message to  other users. The project have this additional features.
1. Reset Forgotten Password using Gmail SMTP server   
2. Profile completion feature using django signals
3. Django channels for messaging

- To run the project follow this commands
1.create virtual env
- pip install virtual env
- virtualenv env
- env\Scripts\avtivate.bat
2. Install django packages
- pip install -r requirements.txt
3.
- python manage.py makemigrations
- python manage.py migrate
4.
- python manage.py createsuperuser
5. run server 
- daphne Simple-Social.asgi:application 




