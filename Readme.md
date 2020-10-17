Dependencies need to install 
1. Python
2. Pip
3. Virtualenv

Packages are install or not to check before running project
-> pip install -r requirements.txt

Process to run the project
1. python views.py (It will run the flask server)
2. Not time to create Tables in terado.db open that file in that location in terminal then using command create 
three table but first open database file which is terado.db
-> .open terado.db
-> Now Create 3 table User, logtable and userdata using below command in terminal
-> CREATE TABLE User(
   	id INTEGER PRIMARY KEY AUTOINCREMENT,
   	username VARCHAR(255),
   	password VARCHAR(255),
	email VARCHAR(255),
	first_name VARCHAR(255),
	last_name VARCHAR(255)
);
CREATE TABLE userdata (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(255),
    dob varchar(255),
    mobile varchar(255),
    address varchar(255),
    user_id int,	
    FOREIGN KEY (user_id)
       REFERENCES User (user_id) 
);
CREATE TABLE logtable (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    path varchar(255),
    user_id int,	
    FOREIGN KEY (user_id)
       REFERENCES User (user_id) 
);
******Now we have running flask server, Database model is created properly in teradb.db*****
3. Now time to hit the API's endpoint created of the project which u will find in view.py 

-> endpoint are:
a) Test api to check flask server is properly running
    -> 127.0.0.1:5000/hello
b) Signup API
  -> 127.0.0.1:5000/user 
  ->  form data fields are (username, password, email, first_name, last_name)
c) Login
  -> 127.0.0.1:5000/login
  ->  form data fields are (username, password)
d) Upload Log File
  -> 127.0.0.1:5000/uploadlog/<string:filename>
  ->  form data fields are (file)
  Note( Choose file from user system name that file as server.log )
e) Upload User Data
  -> 127.0.0.1:5000/user_data/
  ->  form data fields are (name, dob, mobile, address)
f) Get user by id
  -> 127.0.0.1:5000/userbyadmin/<int:id>
g) Get all files upload by particuler user by id
  -> 127.0.0.1:5000/logfiles/<int:id>
