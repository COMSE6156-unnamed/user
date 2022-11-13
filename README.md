
# User Info

  
  

## Environment Setup

  

pip3 install -r requirements.txt

  

## DB Credentials Setup

  

EXPORT DBUSER=<dbusername>

EXPORT DBPW=<dbpassword>

  

## Start user app running

localhost is running at 0.0.0.0:5000

  

python3 app.py

  

## Get all user information

 - Path: `/user`
 - Return value: a list of json objects. `http://localhost:5000/user/all`
 `[ {"user_id": 1, "user_name": "name1}, {"user_id: 2, "user_name": "name2" ]`

## Get user information by user_id

 - Path: `/user/<user_id>`
 - Return value: a list containing a single json object. `http://localhost:5000/user/1`
 - `[ {"user_id": 1, "user_name": "name1} ]`
