#  After connecting the flask app with DB, we need a data structure to read and write from app to table

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Credentials(db.Model):
    __tablename__ = 'credentials'
    uid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String(100))

    def __init__(self,username,password):
        self.username = username
        self.set_password(password)

    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.pwdhash,password)

class Registration(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer,primary_key = True)
    account_number = db.Column(db.String(100))
    cif_number = db.Column(db.String(100))
    branch_code = db.Column(db.Integer())
    country = db.Column(db.String(100))
    phone = db.Column(db.Integer())
    facility = db.Column(db.String(100))

    def __init__(self,accno,cifno,branchcode,country,phone,facility):
        self.account_number = accno
        self.cif_number = cifno
        self.branch_code = branchcode
        self.country = country
        self.phone = phone
        self.facility = facility
        


