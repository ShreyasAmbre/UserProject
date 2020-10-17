from flask_sqlalchemy import SQLAlchemy, Model
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(10), nullable=False)
    last_name = db.Column(db.String(10), nullable=False)

    def getalldata(self):
        return User.query.all()

    def putstudent(self, username, password, email, first_name, last_name):
        user = User(username=username, password=password, email=email,
                         first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def checkuser(self, user):
        username = User.query.filter_by(username=user).first()
        return username


class LogTable(db.Model):
    __tablename__ = 'logtable'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def getalllogs(self):
        return LogTable.query.all()

    def inserlog(self, id, path, user_id):
        print(user_id)
        logs = LogTable(id=id, path=path, user_id=user_id)
        db.session.add(logs)
        db.session.commit()

    def getsinglefile(self, filepath):
        print(filepath)
        file = LogTable.query.filter_by(path=filepath).first()
        print(file, "from model")
        return file

    def getalllogsbyid(self, id):
        print(id)
        files = LogTable.query.filter_by(user_id=id).all()
        return files

class UserData(db.Model):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def getdata(self):
        return UserData.query.all()

    def insertuserdata(self, id, name, dob, mobile, address, user_id):
        userdata = UserData(id=id, name=name, dob=dob, mobile=mobile, address=address, user_id=user_id)
        db.session.add(userdata)
        db.session.commit()

    def getsingledata(self, id):
        userdata = UserData.query.filter_by(user_id=id).first()
        return userdata

    def getuserbydata(self, id):
        user = UserData.query.filter_by(id=id).first()
        return user