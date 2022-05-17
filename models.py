#  After connecting the flask app with DB, we need a data structure to read and write from app to table

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Credentials(db.Model):
    __tablename__ = 'credentials'
    username = db.Column(db.String(100),primary_key = True)
    pwdhash = db.Column(db.String(100))

    def __init__(self,username,password):
        self.username = username
        self.set_password(password)

    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.pwdhash,password)

    def __repr__(self):
        return f'<User: {self.username}>'

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.pwdhash, password_plaintext)



class Registration(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(100),primary_key = True)
    account_number = db.Column(db.String(100))
    cif_number = db.Column(db.String(100))
    branch_code = db.Column(db.Integer())
    country = db.Column(db.String(100))
    phone = db.Column(db.Integer())
    facility = db.Column(db.String(100))

    def __init__(self,username,accno,cifno,branchcode,country,phone,facility):
        self.username = username
        self.account_number = accno
        self.cif_number = cifno
        self.branch_code = branchcode
        self.country = country
        self.phone = phone
        self.facility = facility
    
    def test_new_user_with_fixture(new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email and password_hashed fields are defined correctly
        """
        assert new_user.username == 'sruthi'
        assert new_user.account_number != '1234567890'

class RequestPancard(db.Model):
    __tablename__ = 'panrequest'
    username = db.Column(db.String(100),primary_key = True)
    pan_number = db.Column(db.String(100))

    def __init__(self,username,pan):
        self.username = username
        self.pan_number = pan

class cheq(db.Model):
    __tablename__='cheque'
    ac=db.Column(db.VARCHAR(15),primary_key=True)
    thr=db.Column(db.VARCHAR(15))
    ncheq=db.Column(db.INTEGER)
    nleaf=db.Column(db.INTEGER)
    cheqnum = db.Column(db.INTEGER)
    status = db.Column(db.VARCHAR(15))
    def __init__(self,ac,thr,ncheq,nleaf,cheqnum,status):
        self.ac=ac
        self.thr=thr
        self.ncheq=ncheq
        self.nleaf=nleaf
        self.cheqnum = cheqnum
        self.status = status

class Requestdd(db.Model):
    __tablename__ = 'Requestdd'
    ano=db.Column(db.VARCHAR(15),primary_key=True)
    bname = db.Column(db.String(100),primary_key = True)
    bamou = db.Column(db.String(100),primary_key = True)
    place=db.Column(db.String(100),primary_key = True)

    def __init__(self,ano,bname,bamou,place):
        self.ano= ano
        self.bname = bname
        self.bamou=bamou
        self.place=place

class Account(db.Model):
    __tablename__ = 'account'
    account_number = db.Column(db.String(100))
    date = db.Column(db.Date)
    narration = db.Column(db.String(100))
    refno = db.Column(db.String(100),primary_key = True)
    withdraw = db.Column(db.Integer())
    deposit = db.Column(db.Integer())
    balance = db.Column(db.Integer())
    
    def __init__(self,accno,date,narration,refno,withdraw,deposit,balance):
        self.account_number = accno
        self.date = date
        self.narration = narration
        self.refno = refno
        self.withdraw = withdraw
        self.deposit = deposit
        self.balance = balance
        
class Fdsummary(db.Model):

    tablename = 'fdsummary'
    fd_no =db.Column(db.VARCHAR(3),primary_key=True) 
    account_number=db.Column(db.VARCHAR(50))
    date =db.Column(db.DATE)
    Amount =db.Column(db.Numeric(8,2))
    Validity_in_months =db.Column(db.Numeric(4))
    def init(self,fd_no,account_number,date,Amount,Validity_in_months):
        self.fd_no=fd_no
        self.account_number=account_number
        self.date=date
        self.Amount=Amount
        self.Validity_in_months=Validity_in_months


