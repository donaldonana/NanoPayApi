# Profile REST API

### requirements :
1. windows 10.x OS or later 
2. Python 3.7.X or one later stable version , the download link 👉https://www.python.org/downloads/👈

### To Run Project:
1. Clone it : **git clone https://github.com/donaldonana/api_project.git**
2. Move to the project directory : **cd api_project**
3. Create the virtual environment :  **python -m venv ./env**
4. Activate the virtual environment, just run the activate bacht file : **activate**
5. Install the requirement library with requirements.txt : **pip install -r requirements.txt**
6. Create the initials migrations : **python manage.py makemigrations**
7. Run the migrations : **python manage.py migrate**
8. Create the super user : **python manage.py createsuperuser**
9. right, now you can start the server : **python manage.py runserver**

Now you can acces to the Django admin Dashbord in your broswer with the link : http://127.0.0.1:8000/

### ready api endpoint
1. **method**: get **link** : http://127.0.0.1:8000/api/UserProfile/ (get all the user)
2. **method**: get **link** :http://127.0.0.1:8000/api/UserProfile/id (retreive the specific user)
3. **method**: post **link** :http://127.0.0.1:8000/api/UserProfile/ (post the user with the following params)
    * name : char field
    * email : email field
    * last_name : char field
    * first_name : char field
    * contact : char field

4. ....


