from itertools import islice

def chunks(data, SIZE=10000):
   it = iter(data)
   for i in range(0, len(data), SIZE):
      yield {k:data[k] for k in islice(it, SIZE)}


#  import Flask class
from urllib import response
from flask import Flask, redirect,render_template,request, url_for,session
from models import Registration, db,Credentials
from forms import SignupForm,OTPForm,ATMForm,UserForm,PancardForm

# Create instance from Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dbpassword@localhost:5432/Online-Banking'
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdZVdMeAAAAAIMHMxsdYVD6PDYdGL-C-LaoOPmT'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdZVdMeAAAAAPtHZZEVnGlLHI7SlENOrjuETY2V'

db.init_app(app)

# To create secure forms
app.secret_key = "development-key"

@app.route("/")
def home():    
    session.pop('username',None)
    session.pop('reg_form',None)
    return 'render_template("home.html")'

@app.route("/success")
def success():
    if 'reg_form' not in session:
            return redirect(url_for('register'))
    return render_template("success.html")

@app.route("/username",methods=['GET','POST'])
def username():
    if request.method == 'GET':
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success'))
        
        form = UserForm()
        return render_template("username.html",form=form)
    elif request.method == 'POST':
        form = UserForm(request.form) 
        if form.validate() == False:
            return render_template('username.html',form=form)
        else:
            newuser = Credentials(form.username.data,form.password.data)   # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB

            session['username'] = form.username

            reg_form = session['reg_form']
            newuser = Registration(reg_form['accno'],reg_form['cifno'],reg_form['branchcode'],reg_form['country'],reg_form['phone'],reg_form['facility'])   # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB 


            

            return redirect(url_for('success'))

@app.route("/atm",methods=['GET','POST'])
def atm():
    if request.method == 'GET':
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success'))
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
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success'))
        form = OTPForm()
        return render_template("otp.html",form=form,param=param)
    elif request.method == 'POST':
        form = OTPForm(request.form) 
        if form.validate() == False:
            return render_template('otp.html',form=form,param=param)
        else:
            # newuser = User(form.accno.data,form.cifno.data,form.branchcode.data,form.country.data)   # Create new user
            # db.session.add(newuser) # Add new user to DB
            # db.session.commit()     # Save changes to DB

            # session['email'] = newuser.email
            if param == 'register':
                return redirect(url_for('atm'))

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        form = SignupForm(request.form) 
        if form.validate() == False:
            return render_template('register.html',form=form)
        else:
            # newuser = Registration(form.accno.data,form.cifno.data,form.branchcode.data,form.country.data,form.phone.data,form.facility.data)   # Create new user
            # db.session.add(newuser) # Add new user to DB
            # db.session.commit()     # Save changes to DB 

            session['reg_form'] = form.data
            print(session['reg_form'])
            return redirect(url_for('otp',param='register'))
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('success'))
        form = SignupForm()    
        return render_template('register.html',form=form)

if __name__ == "__main__":    
    app.run(debug=True) 
