# Time Management System
* a user can register and login
* a user can create, update, delete a task
* a user can set preferred hour for a day

### Author
* Jongwook Kim fantazic@gmail.com

### HOWTO
* clone git
* migrate for DB
* run a server
    * default 8888 port
    * localhost:8888/tms
* you should set nginx for static files and javascripts

```
git clone ...
cd tms
python manage.py makemigrations
python manage.py migrate
python manager.py runserver
```

### Package
* app: Django project
* tms: a front end app for templates and javascripts
* api: a REST API app for authentication and all other functions with models

### Back End
* Django
* SQLite

### Front End
* Vue.js
    * Vue Resource for Ajax
* Bootstrap

### Demo site
* [catlog/tms](http://catlog.kr/tms/)
    * nginx + gunicorn + django
