<p align="left">
  <a href="#">
    <img 
      alt="enel-telecontrol-logo" 
      src="enel-telecontrol-logo.png" 
      width="240"/>
  </a>
</p>

**Enel Telecontrole Web**: Web Plataform written in python for managing the electric point project process.
Version: **1.0**
***
# Table of Contents
* [Getting Started](#getting-started)
    * [Unix version comparison](#unix-version-comparison)
    * [Installation process](#installation-process)
    * [Usage](#usage)
    * [Examples](#examples)
* [License](#license)
***
## Getting Started
#### Development Environment
1. Create postgreSQL database table
```Shell
psql -U postgres
create database telecontrol;
```
2. Set virtual environment (example with virtualenv-wrapper):
```Shell
mkvirtualenv telecontrol
workon telecontrol
```
3. Install requirements:
```Shell
pip install -r requirements
```
4. Run Django migrations
```Shell
python manage.py migrate
```
5. Create admin superuser:
```Shell
python manage.py createsuperuser
```
6. Run development server
```Shell
python manage.py runserver
```