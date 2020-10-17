import json
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources import Hello, Userapi, Login, UploadLog, Logout, User_Data, UserByAdmin, LogFileByAdmin
from model import *


UPLOAD_FOLDER = '/home/shreyas/Desktop/TestProject/static'

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terado.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()


app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api.add_resource(Hello, "/hello")
api.add_resource(Userapi, "/user")
api.add_resource(Login, "/login")
api.add_resource(UploadLog, "/uploadlog", "/uploadlog/<string:filename>")
api.add_resource(Logout, "/logout")
api.add_resource(User_Data, "/user_data")
api.add_resource(UserByAdmin, '/userbyadmin/<int:id>')
api.add_resource(LogFileByAdmin, '/logfiles/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)
