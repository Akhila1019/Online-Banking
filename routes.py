#  import Flask class
from flask import Flask, redirect,render_template,request, url_for,session
from models import Registration, db,Credentials,RequestPancard
from forms import SignupForm,OTPForm,ATMForm,UserForm,PancardForm,EnterPanForm
from getOTP import returnOTP

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
    session.pop('pan_card',None)
    session.pop('pan_form',None)
    return 'render_template("home.html")'

@app.route("/success<param>")
def success(param):
    if 'reg_form' not in session:
            return redirect(url_for('register'))
    if 'username' not in session:
            return redirect(url_for('register'))
    if param == 'username':
        return render_template("success.html",msg="Successfully registered for Internet Banking :)")
    if param == 'pancard':
        if 'pan_card' not in session:
            return redirect(url_for('pancard'))
        return render_template("success.html",msg="Pan card add/update request is accepted successfully and will be validated by branch shortly.")

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

            newuser = Credentials(form.username.data,form.password.data)   # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB
            
            session['username'] = request.form.get('username')
            reg_form = session['reg_form']
            
            newuser = Registration(session['username'],reg_form['accno'],reg_form['cifno'],reg_form['branchcode'],reg_form['country'],reg_form['phone'],reg_form['facility'])   # Create new user
            db.session.add(newuser) # Add new user to DB
            db.session.commit()     # Save changes to DB 
            return redirect(url_for('success',param='username'))

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
        if 'reg_form' not in session:
            return redirect(url_for('register'))
        elif 'username' in session:
            return redirect(url_for('success',param='username'))
        form = OTPForm()
        returnOTP()
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
            session['otp_form'] = form.data
            if param == 'register':
                return redirect(url_for('atm'))
            elif param == 'pancard':
                return redirect(url_for('panenter'))

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        form = SignupForm(request.form) 
        if form.validate() == False:
            return render_template('register.html',form=form)
        else:
            # newuser = Registration(form.accno.data,form.cifno.data,form.branchcode.data,form.country.data,form.phone.data,form.facility.data)   # Create new user
            # db.session.add(newuser) # Add new user to DB
            # db.session.commit()     # Save changes to DB 
            session['reg_form'] = form.data
            return redirect(url_for('otp',param='register'))
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('success',param='username'))
        form = SignupForm()    
        return render_template('register.html',form=form)

@app.route("/pancard",methods=['GET','POST'])
def pancard():
    if request.method == 'POST':
        form = PancardForm(request.form)
        form.username.data = session['username']
        if form.validate()==False:
            return render_template('pancard.html',form=form)
        else:
            session['pan_card'] = form.data
            return redirect(url_for('panenter'))
    elif request.method == 'GET':
        if 'pan_form' in session:
            return redirect(url_for('success',param='pancard'))
        form = PancardForm()
        return render_template('pancard.html',form=form)

@app.route("/panenter",methods=['GET','POST'])
def panenter():
    if request.method == 'POST':
        form = EnterPanForm(request.form) 
        if form.validate() == False:
            return render_template('panenter.html',form=form)
        else:
            session['pan_form'] = form.data
            return redirect(url_for('confirmpan'))
    elif request.method == 'GET':
        if 'pan_card' not in session:
            return redirect(url_for('pancard'))
        if 'pan_form' in session:
            return redirect(url_for('success',param='pancard'))
        form = EnterPanForm()    
        return render_template('panenter.html',form=form)

@app.route("/confirmpan",methods=['GET','POST'])
def confirmpan():
    if request.method == 'POST':
        newrequest = RequestPancard(session['username'],session['pan_form']['pan'])   # Create new user
        db.session.add(newrequest) # Add new user to DB
        db.session.commit()     # Save changes to DB
        return redirect(url_for('success',param='pancard'))
    elif request.method == 'GET': 
        if 'pan_card' not in session:
            return redirect(url_for('pancard')) 
        username = session['username']
        user = Registration.query.filter_by(username=username).first()
        cifno = user.cif_number
        return render_template('confirmpan.html',details=[username,cifno])

# @app.route('/sms', methods=['POST'])
# def sms():
#     reg_form = session['reg_form']
#     number = reg_form['phone']
#     otp = randint(1000,9999)
#     account_sid = "AC390d3a533486540545dc51945f754305"
#     auth_token = "904b88c315e940f745b23585b3de8035"

#     client = Client(account_sid,auth_token)

#     msg = client.messages.create(
#         body = f"Your OTP is {otp}",
#         from_ = "+15156047488",
#         to = "+91"+str(number)
#     )

if __name__ == "__main__":    
    app.run(debug=True) 
