import os, re
from flask import Flask, session, request, send_file
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from model import User, LogTable, UserData


class Hello(Resource):
    def get(self):
        return {"msg": "Hello"}


# Requestparser Object created to accespt the student arguments
Student_put_obj = reqparse.RequestParser()

# argument created using object
# Student_put_obj.add_argument("id", type=int, help="Name of the student")
Student_put_obj.add_argument("username", type=str, help="Name of the student")
Student_put_obj.add_argument("password", type=str, help="Age of the student")
Student_put_obj.add_argument("email", type=str, help="Age of the student")
Student_put_obj.add_argument("first_name", type=str, help="Gender of the student")
Student_put_obj.add_argument("last_name", type=str, help="Gender of the student")

resource_fields = {
    "id": fields.Integer(),
    "username": fields.String(),
    "password": fields.String(),
    "email": fields.String(),
    "first_name": fields.String(),
    "last_name": fields.String()
}


class Userapi(Resource):
    # Code to get data
    @marshal_with(resource_fields)
    def get(self):
        result = list(User.getalldata(self))
        return result

    # Code to insert data
    # @marshal_with(resource_fields)
    def put(self):
        args = Student_put_obj.parse_args()
        # print(args.username)
        user = User.checkuser(self, args.username)
        print(user, "I m User")
        if user:
            return {"msg": "User Already Exsist"}, 500
        else:
            email = args.email
            print(email)
            valid = re.findall(r"[^@]+@[^@]+\.[^@]+", email)
            print(valid, "Valid")
            if len(valid) == 1:
                encpassword = generate_password_hash(args.password, method='sha256')
                User.putstudent(self, args.username, encpassword, args.email, args.first_name, args.last_name)
                return {"msg": "User Created"}, 201
            else:
                return {"msg": "Email id not valid"}, 500


User_login_obj = reqparse.RequestParser()

User_login_obj.add_argument("username", type=str, help="Name of the student")
User_login_obj.add_argument("password", type=str, help="Name of the student")


class Login(Resource):
    def post(self):
        args = Student_put_obj.parse_args()
        username = args.username
        password = args.password
        encpassword = generate_password_hash(args.password, method='sha256')

        user = User.checkuser(self, username)
        print(user)
        auth_val = check_password_hash(user.password, password)
        print(auth_val)

        if username == user.username:
            session['username'] = user.id
            #     print(session)
            return {"msg": "User Logged In"}, 200
        else:
            return 500
        # return 200


resource_fields2 = {
    "id": fields.Integer(),
    "path": fields.String(),
    "user_id": fields.Integer(),
    "filedata": fields.String()
}

UserLog_obj = reqparse.RequestParser()
UserLog_obj.add_argument("id", type=str, help="Name of the student")


class UploadLog(Resource):
    def post(self):
        args = UserLog_obj.parse_args()
        print(session)
        if session:
            log_file = request.files['file']
            print(log_file)
            from views import app
            print(app.config['UPLOAD_FOLDER'])
            log_file.save(os.path.join(app.config['UPLOAD_FOLDER'], log_file.filename))
            path = app.config['UPLOAD_FOLDER'] + "/" + log_file.filename
            user_id = session['username']
            print(user_id)
            id = args.id
            print(id)
            LogTable.inserlog(self, id, path, user_id)
            return {"msg": "File Uploaded"}, 200
        else:
            return 500

    @marshal_with(resource_fields2)
    def get(self, filename):
        if session:
            # filename = request.form['filename']
            print(filename, "---------------")
            if filename:
                from views import app
                path = app.config['UPLOAD_FOLDER']
                filepath = path + "/" + filename
                result = LogTable.getsinglefile(self, filepath)
                print(result)
                if result:
                    # path2 = path + "/" + filename
                    file = open(filepath, "r")
                    data = file.read()
                    print(data)
                    # return {"filedata": data}, 200
                    return {"filedata": data}, 200
                else:
                    return 500
            else:
                result = LogTable.getalllogs(self)
                return result


UserData_obj = reqparse.RequestParser()
UserData_obj.add_argument("id", type=int, help="Name of the student")
UserData_obj.add_argument("name", type=str, help="Name of the student")
UserData_obj.add_argument("dob", type=str, help="Name of the student")
UserData_obj.add_argument("mobile", type=str, help="Name of the student")
UserData_obj.add_argument("address", type=str, help="Name of the student")

resource_fields3 = {
    "id": fields.Integer(),
    "name": fields.String(),
    "dob": fields.String(),
    "mobile": fields.String(),
    "address": fields.String(),
    "user_id": fields.String(),
}


class User_Data(Resource):
    def post(self):
        if session:
            args = UserData_obj.parse_args()
            user_id = session['username']
            # print
            UserData.insertuserdata(self, args.id, args.name, args.dob, args.mobile, args.address, user_id)
            return 200
        else:
            return 500

    @marshal_with(resource_fields3)
    def get(self):
        if session:
            id = session['username']
            print(id)
            userdata = UserData.getsingledata(self, id)
            return userdata


class UserByAdmin(Resource):
    @marshal_with(resource_fields3)
    def get(self, id):
        print(id)
        # args = Userbyadmin_obj.parse_args()
        # print(args)
        userdata = UserData.getuserbydata(self, id)
        return userdata


class LogFileByAdmin(Resource):
    @marshal_with(resource_fields2)
    def get(self, id):
        result = LogTable.getalllogsbyid(self, id)
        print(result)
        return result, 200

class Logout(Resource):
    def get(self):
        session.pop('username')
        return 200


