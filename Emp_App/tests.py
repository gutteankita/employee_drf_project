from Emp_App.models import *
import json
import requests

register_url="http://127.0.0.1:8000/api/user/register/"

#Get User
def get_user_record(id=None):
    data={}
    if id is not None:
        data={"id":id}
    jsondata=json.dumps(data)
    r=requests.get(url=register_url, data=jsondata, headers= {'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)

# All Records    
# get_user_record()

# Particular Record
# get_user_record(17)


#Create User
def post_user_record():
    data = {
        "username": "Krishna",
        "email": "krishna@gmail.com",
        "password": "krishna",
        "is_active": True,
        "is_admin": False,
        "is_user": True,
    }
    jsondata=json.dumps(data)
    r=requests.post(url=register_url,data=jsondata, headers= {'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)
# post_user_record()

# Update User
def update_user_record():
    data = {
        "id": "10",
        "username": "Krish",
        "email": "krish@gmail.com",
        "password": "krish",
        "is_active": True,
        "is_admin": False,
        "is_user": True,
    }
    jsondata=json.dumps(data)
    r=requests.put(url=register_url,data=jsondata, headers= {'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)    
# update_user_record()


# Delete User
def delete_user_data():
    data={"id":"18"}
    jsondata=json.dumps(data)
    r=requests.delete(url=register_url,data=jsondata, headers= {'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)
# delete_user_data()

# Login User
def login_user():
    login_url = 'http://127.0.0.1:8000/api/user/login/'
    data =  {
            'email':'ankit@gmail.com',
            'password': 'ankit',
        }
    r=requests.post(url=login_url,data=data)
    data=r.json()
    return str(data['token'])
# login_user()



emp_url="http://127.0.0.1:8000/api/user/employee/"

#Get Employee
def get_record(id=None):
    data={}
    if id is not None:
        data={"id":id}
    jsondata=json.dumps(data)
    r=requests.get(url=emp_url, data=jsondata, headers= {'Authorization':'jwt ' + login_user(), 'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)

# All Records    
# get_record()

# Particular Record
# get_record(1)


#Create Employee
def post_record():
    data = {
        "name": "Krishna",
        "age": 34,
        "gender": "M",
        "department": "IT",
        "salary": 40000,
    }
    jsondata=json.dumps(data)
    r=requests.post(url=emp_url,data=jsondata, headers= {'Authorization':'jwt ' + login_user(), 'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)
# post_record()

# Update Employee
def update_record():
    data = {
        'id':9,
        'name': 'Krishna',
        "age": 14,
        "gender": "M",
        "department": "IT",
        "salary": 40000,
    }
    jsondata=json.dumps(data)
    r=requests.put(url=emp_url,data=jsondata, headers= {'Authorization':'jwt ' + login_user(), 'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
# update_record()


# Delete Employee
def delete_data():
    data={'id':"4"}
    jsondata=json.dumps(data)
    r=requests.delete(url=emp_url,data=jsondata, headers= {'Authorization':'jwt ' + login_user(), 'Accept': 'application/json',
        'Content-Type': 'application/json'})
    data=r.json()
    print(data)
# delete_data()