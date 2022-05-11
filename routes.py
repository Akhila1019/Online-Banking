#  import Flask class
import csv
from random import randint
from flask import Flask, Response,redirect,render_template,request,url_for,session,flash,send_file
from models import Account, Registration, db,Credentials,RequestPancard,cheq
from forms import ChangePwdForm,ChequeForm,ForgotForm,NewpwdForm,RequestForm,StopchequeForm,PancardForm,EnterGstForm
from forms import HomeForm,ACForm,StatusForm,ViewAcBalForm,UserForm,ATMForm,OTPForm,SignupForm,EnterPanForm,LoginForm,AmountMonthForm
from getOTP import return_otp
from werkzeug.security import generate_password_hash
import datetime
import psycopg2
import secrets
import string


# Create instance from Flask class
app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dbpassword@localhost:5432/Online-Banking'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ooiymqfeiassio:70522e6829fe4c18cf8db346f2599ba5f9aef7e8e12eb87be78a44606710fe93@ec2-54-164-40-66.compute-1.amazonaws.com:5432/d7r3h476bmi0rf'
db.init_app(app)

# To create secure forms
app.secret_key = "development-key"
prevcur = 'prevcurrstatement.html'
success_page = 'success.html'
v = 'view.html'
vac = 'view_ac_bal.html'
ac5 = 'ac5years.html' 
ymd = "'%Y-%m-%d'"

def checkparam1(param):
    if param == 'username':
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        if 'username' not in session:
            return redirect(url_for('register'))
        return render_template(success_page,msg="Successfully registered for Internet Banking :)")

def checkparam2(param):
    if param == 'pancard':
        if 'pan_card_form' not in session:
            return redirect(url_for('pancard'))
        return render_template(success_page,msg="Pan card add/update request is accepted successfully and will be validated by branch shortly.")
    if param == 'forgot_pwd':
        if 'forgot_form' not in session:
            return redirect(url_for('forgot_pwd'))
        return redirect(url_for('newpwd'))

def checkparam3(param):
    if param == 'change_pwd':
        msg = "Password changed successfully."
    elif param == 'ddreq':
        msg = "DD request was made successfully."
    elif param == 'stopcheque':
        msg = "Stop payment of cheque request was made successfully"
    elif param == 'cheque':
        msg = "Request for cheque was made successfully"
    elif param == 'home':
        msg = "Logged Out successfully."
    return msg

@app.route("/")
def home1():
    if 'login_form' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('success',param='home'))

@app.route("/home",methods=['GET','POST'])
def home():
    if 'login_form' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        form = HomeForm()
        return render_template('home1.html',form=form)
    elif request.method == 'POST':
        session.pop('login_form',None)
        session.pop('reg_form',None)
        session.pop('username',None)
        session.pop('forgot_form',None)
        session.pop('change_form',None)
        session.pop('pan_card_form',None)
        session.pop('pan_enter_form',None)
        return redirect(url_for('success',param='home'))

@app.route("/success<param>")
def success(param):
    checkparam1(param)
    checkparam2(param)
    msg = checkparam3(param)
    if param == 'newpwd'and 'forgot_form' not in session:
            return redirect(url_for('forgot_pwd'))
    elif param == 'newpwd'and 'forgot_form' in session:
        msg = "Password updated successfully."

    return render_template(success_page,msg=msg)

@app.route("/username",methods=['GET','POST'])
def username():
    if request.method == 'GET':
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success',param='username'))
        form = UserForm()
        return render_template("username.html",form=form)
    elif request.method == 'POST':
        form = UserForm(request.form)
        if form.validate() == False:
            return render_template('username.html',form=form)
        else:
            newuser = Credentials(form.username.data,form.password.data)  # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB        
            session['username'] = request.form.get('username')
            reg_form = session['reg_form']            
            newuser = Registration(session['username'],reg_form['accno'],reg_form['cifno'],reg_form['branchcode'],reg_form['country'],reg_form['phone'],reg_form['facility'])   # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB 
            return redirect(url_for('success',param='username'))

@app.route("/stopcheque",methods=['GET','POST'])
def stopcheque():
    if request.method == 'POST':
        form = StopchequeForm(request.form) 
        if form.validate() == False:
            return render_template('stop cheque.html',form=form)
        else:
            return redirect(url_for('success',param='stopcheque'))
    elif request.method == 'GET':
        
        form = StopchequeForm()    
        return render_template('stop cheque.html',form=form)

@app.route("/atm",methods=['GET','POST'])
def atm():
    if request.method == 'GET':
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success',param='username'))
        form = ATMForm()
        return render_template("atm.html",form=form)
    elif request.method == 'POST':
        form = ATMForm(request.form) 
        if form.validate() == False:
            return render_template('atm.html',form=form)
        else:
            if form['atm'].data == 'yes':
                return redirect(url_for('username'))
            else:
                return render_template("bank.html")

@app.route("/otp/<param>",methods=['GET','POST'])
def otp(param):
    if request.method == 'GET':
        if param == 'forgot_pwd' and 'forgot_form' not in session:
            return redirect(url_for('forgot_pwd'))
        elif param == 'register' and'reg_form' not in session:
            return redirect(url_for('register'))
        form = OTPForm()
        return render_template("otp.html",form=form,param=param)
    elif request.method == 'POST':
        form = OTPForm(request.form) 
        if form.validate() == False:
            return render_template('otp.html',form=form,param=param)
        else:
            if param == 'register':
                return redirect(url_for('atm'))
            elif param == 'forgot_pwd':
                return redirect(url_for('newpwd'))

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        form = SignupForm()    
        return render_template('register.html',form=form)
    elif request.method == 'POST':
        form = SignupForm(request.form) 
        if form.validate() == False:
            return render_template('register.html',form=form)
        else:
            session['reg_form'] = form.data
            return_otp(session['reg_form'])
            return redirect(url_for('otp',param='register'))
    

@app.route("/pancard",methods=['GET','POST'])
def pancard():
    uname = session['username']
    user = RequestPancard.query.filter_by(username=uname).first()
    if user is not None:
        flash("PAN already exists")
        return redirect(url_for('home'))
    if 'login_form' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        if 'pan_enter_form' in session and'confirm_pan_form' in session:
            return redirect(url_for('success',param='pancard'))
        form = PancardForm()
        return render_template('pancard.html',form=form)
    elif request.method == 'POST':
        form = PancardForm(request.form)
        form.username.data = session['username']
        if form.validate()==False:
            return render_template('pancard.html',form=form)
        else:
            session['pan_card_form'] = form.data
            return redirect(url_for('panenter'))
    

@app.route("/panenter",methods=['GET','POST'])
def panenter():
    if 'login_form' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        if 'pan_enter_form' in session and 'confirm_pan_form' in session:
            return redirect(url_for('success',param='pancard'))
        form = EnterPanForm()   
        uname = session['username']
        user = Registration.query.filter_by(username=uname).first()
        cifno = user.cif_number
        accno = user.account_number
        return render_template('panenter.html',form=form,details=[accno,cifno])
    elif request.method == 'POST':
        form = EnterPanForm(request.form)
        form.username.data = session['username'] 
        uname = session['username']
        user = Registration.query.filter_by(username=uname).first()
        cifno = user.cif_number
        accno = user.account_number
        if form.validate() == False:
            return render_template('panenter.html',form=form,details=[accno,cifno])
        else:
            session['pan_enter_form'] = form.data
            return redirect(url_for('confirmpan'))
    

@app.route("/confirmpan",methods=['GET','POST'])
def confirmpan():
    if request.method == 'POST':
        session['confirm_pan_form'] = 'form.data'
        newrequest = RequestPancard(session['username'],session['pan_enter_form']['pan'])   # Create new user
        db.session.add(newrequest) # Add new user to DB
        db.session.commit()     # Save changes to DB
        return redirect(url_for('success',param='pancard'))
    elif request.method == 'GET':
        if 'pan_card_form' not in session:
            return redirect(url_for('pancard')) 
        username = session['username']
        user = Registration.query.filter_by(username=username).first()
        cifno = user.cif_number
        return render_template('confirmpan.html',details=[username,cifno])
       
@app.route("/entergst",methods=['GET','POST'])
def gst():
    if request.method == 'POST':
        form = EnterGstForm(request.form) 
        if form.validate() == False:
            return render_template('addgst.html',form=form)
        else:
            return redirect(url_for('success')) 
    elif request.method == 'GET':
            form = EnterGstForm()    
            return render_template('addgst.html',form=form)

@app.route("/change_pwd",methods=['GET',"POST"])
def change_pwd():
    if request.method=='GET':
        form=ChangePwdForm()
        return render_template('change_pwd.html',form=form)
    elif request.method=='POST':
        form=ChangePwdForm(request.form)
        if form.validate()==False:
            return render_template('change_pwd.html',form=form)
        session['change_form'] = form.data
        username = request.form['username']
        user = Credentials.query.filter_by(username=username).first()
        user.pwdhash = generate_password_hash(request.form['new1'])
        db.session.commit()
        return redirect(url_for('success',param='change_pwd'))
         
@app.route("/cheque",methods=['GET','POST'])
def cheque():
    if request.method == 'GET':
        form = ChequeForm()
        return render_template("cheq.html",form=form) 
    elif request.method == 'POST':
        form=ChequeForm(request.form)
        if form.validate() == False:
            return render_template("cheq.html",form=form)
        num = string.digits
        randomnum = ''.join(secrets.choice(num) for i in range(8))
        cheqnum = randomnum
        status = 'Not used'
        newuser = cheq(form.ac.data,form.thr.data,form.ncheq.data,form.nleaf.data,cheqnum,status)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('success',param='cheque'))

@app.route("/ddreq",methods=['GET','POST'])
def ddreq():
    if request.method == 'GET':
        form = RequestForm()
        return render_template("requestdd.html",form=form)
    elif request.method == 'POST':
        form = RequestForm(request.form) 
        if form.validate() == False:
            return render_template('requestdd.html',form=form)
        else:
            return redirect(url_for('success',param='ddreq'))

@app.route("/forgot_pwd",methods=['GET','POST'])
def forgot_pwd():
    if request.method == 'GET':
        form = ForgotForm()    
        return render_template('forgot_pwd.html',form=form)
    elif request.method == 'POST':
        form = ForgotForm(request.form) 
        if form.validate() == False:
            return render_template('forgot_pwd.html',form=form)
        else:
            session['forgot_form'] = form.data
            session['accno'] = form.accno.data
            return_otp(session['forgot_form'])
            return redirect(url_for('otp',param='forgot_pwd')) 
    

@app.route("/newpwd",methods=['GET','POST'])
def newpwd():
    if request.method == 'GET':
        if 'forgot_form' not in session:
            return redirect(url_for('forgot_pwd'))
        form = NewpwdForm()
        return render_template("newpwd.html",form=form)
    elif request.method == 'POST':
        form = NewpwdForm(request.form) 
        if form.validate() == False:
            return render_template('newpwd.html',form=form)
        else:
            acc = Registration.query.filter_by(account_number=session['accno']).first()
            username = acc.username
            user = Credentials.query.filter_by(username=username).first()
            user.pwdhash = generate_password_hash(request.form['pwd'])
            db.session.commit()
            return redirect(url_for('success',param='newpwd')) 

@app.route("/tos",methods=['GET','POST'])
def tos():
    if request.method == 'GET':
        return render_template("terms of services.html")
    elif request.method == 'POST':
        return redirect(url_for('username')) 

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login_form' in session:
            return redirect(url_for('home'))
        form = LoginForm()    
        return render_template('login.html',form=form)
    elif request.method == 'POST':
        form = LoginForm(request.form) 
        if form.validate() == False:
            return render_template('login.html',form=form)
        else:
            session['username'] = form.username.data
            session['login_form'] = form.data     
            return redirect(url_for('home')) 
    
@app.route("/acc",methods=['GET','POST'])
def acc():
    if request.method == 'GET':
        form = ACForm() 
        return render_template(ac5,form=form)
    elif request.method == 'POST':
        form = ACForm(request.form)
        if form.validate() == False:
            return render_template(ac5,form=form)        
        acc = Registration.query.filter_by(username=session['username']).first()
        accno = acc.account_number
        curr = datetime.datetime.strptime(request.form['period'], ymd)
        lastyear = curr.year-5
        lastmon = curr.month
        lastday = curr.day
        last = datetime.date(lastyear,lastmon,lastday)
        accdetails = Account.query.filter(Account.date.between(last,curr)).all()
        return render_template(ac5,form=form,accdetails=accdetails,accno = accno)

@app.route("/pay",methods=['GET','POST'])
def payment():
    return render_template('payment.html')

@app.route("/thanks")
def thanks():
    return render_template('thanks.html')

@app.route('/download_csv')
def download_csv():
    query = """
        SELECT
        * FROM account
    """
    try:
        acc = Registration.query.filter_by(username=session['username']).first()
        accno = acc.account_number
        conn = psycopg2.connect(database="Online-Banking", user="postgres", host="localhost", password="dbpassword")
        cur = conn.cursor()
        cur.execute(query)
        with open('result.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Account Number','Date','Narration','Reference Number','Deposit','Withdraw','Balance'])
            for row in cur.fetchall():
                if(row[0]==accno):
                    writer.writerow(row)
            f.seek(0)
            r = Response(f, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=result.csv"})
            print(r)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

    path = "result.csv"
    return send_file(path, as_attachment=True)

@app.route("/view",methods=['GET','POST'])
def view():
    if request.method == 'POST':
        form = StatusForm(request.form) 
        if form.validate() == False:
            return render_template(v,form=form)
        session['cheqnum']=form.cheqnum.data
        acc= cheq.query.filter_by(cheqnum = session['cheqnum']).first()
        bal=acc.status
        return render_template(v,form=form,bal=bal)    
    elif request.method == 'GET':
        form = StatusForm()    
        return render_template(v,form=form)

@app.route("/view_ac_bal",methods=['GET','POST'])  
def accbal():
    if request.method=='GET':
      form=ViewAcBalForm()
      return render_template(vac,form=form)
    elif request.method=='POST':
      form=ViewAcBalForm(request.form)
      if form.validate()==False:
        return render_template(vac,form=form)
      session['ac']=form.ac.data
      acc= Account.query.filter_by(account_number=session['ac']).first()
      bal=acc.balance
      return render_template(vac,form=form,bal=bal)

@app.route("/curprev",methods=['GET','POST'])
def curprev():
     if request.method == 'GET':
        form =  AmountMonthForm() 
        return render_template(prevcur,form=form)
     elif request.method == 'POST':
        form =  AmountMonthForm(request.form)
        if form.validate() == False:
            return render_template(prevcur,form=form)
        
        acc = Registration.query.filter_by(username=session['username']).first()
        accno = acc.account_number
        period1 = datetime.datetime.strptime(request.form['period1'], ymd)
        period2 = datetime.datetime.strptime(request.form['period2'], ymd)
        if(period2.year - period1.year <=1 and period2.month-period1.month<=1):
            accdetails = Account.query.filter(Account.date.between(period1,period2)).all()
            print(accdetails)
            return render_template(prevcur,form=form,accdetails=accdetails,accno = accno)
        else:
            return render_template(prevcur,form=form)
if __name__ == "__main__": 
    app.run(debug=True) 
