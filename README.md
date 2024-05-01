[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/mn6pV4Nk)

# SAM's Documentation - Milestone 4 

# READ FIRST !!! Please... 

## POSTMAN DOCUMENTATION

[POSTMAN-SAM](https://documenter.getpostman.com/view/32945632/2sA2xmVqdE)
`https://documenter.getpostman.com/view/32945632/2sA2xmVqdE`

> USING ENUM FOR TYPE:
(you can only choose ONE of three below to POST)
>> Account Type: "savings", "trading", and "platinum"
>> Transaction Type: "transfer", "deposit", and "withdrawal"

>USING RANDINT FOR account_number: so when you POST it, your account_number will automattically turn into random integer.

## My Little Notes
Please Check
1. LOGIN
2. Register
3. Add new Product
4. Search Product
5. See Reviews
6. edit product data
7. Delete data
8. Give Response
9. Back link and logout

### INSTALL THE REQUIREMENTS

> `pip install -r requirements.txt`
> To run the app
>> `flask --app index run --debug `

- The Requirement That I use:

```reqirement.txt
bcrypt==4.1.2
blinker==1.7.0
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
docopt==0.6.2
Flask==3.0.2
Flask-JWT-Extended==4.6.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
idna==3.6
itsdangerous==2.1.2
Jinja2==3.1.3
MarkupSafe==2.1.5
mysql-connector-python==8.3.0
PyJWT==2.8.0
python-dotenv==1.0.1
requests==2.31.0
SQLAlchemy==2.0.25
typing_extensions==4.9.0
urllib3==2.2.0
Werkzeug==3.0.1
yarg==0.1.9
```

### ADD YOUR .ENV

use this and insert as the same as your mySQL WorkBench configuration
>MAKE A FILE NAME: .env at the first folder when you open it. 
```
DATABASE_USERNAME=(your root name)
DATABASE_PASSWORD= (your password)
DATABASE_URL=(your address like 127.0.0.1)
DATABASE_NAME=(your database's name)

SECRET_KEY=MYSECRETKEY
```

### Don't Forget tu RUN - USE DATABASE first at MySQL WorkBench
