# Capstone-2k21-CPG33

## Guide to Use Project
#### Install

```
git clone https://github.com/Tewatia5355/Capstone-2k21-CPG33.git
```


#### Usage

##### Secret variables

Before running the application you need to fill 3 variables in ```eng\info.py``` 
```
EMAIL_HOST =  ## enter email host, i.e. 'smtp.gmail.com'
EMAIL_HOST_USER = ## enter email address
EMAIL_HOST_PASSWORD = ## enter passwrod of email address
```


For first time:
```
cd Capstone-2k21-CPG33
pip install -r requirements.txt 
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver
```

For regular usage:
```
cd Capstone-2k21-CPG33
python manage.py runserver
```
