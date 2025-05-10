## Install pipenv library (If not existing)
```bash
pip install pipenv
```

## Run Virtual Environment
```bash
pipenv shell
```

## Create .env based on .env.example

## Install Dependencies
```bash
pipenv install -r requirements.txt
```

## Generate Secret Key
```bash
py generate-key.py
```

## Create New App (Django Built-In)
```bash
django-admin startapp 'app-name'
```

## Migration (Django Built-In)
```bash
py manage.py makemigrations
py manage.py migrate
```

## Run Development Server (Django Built-In)
```bash
py manage.py runserver
```

## Update requirements.txt (Contains Dependencies)
```bash
pipenv requirements > requirements.txt
```