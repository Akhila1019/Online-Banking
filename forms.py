from flask_wtf import Form,RecaptchaField
from wtforms import StringField,SubmitField,SelectField,RadioField,BooleanField,PasswordField
from wtforms.validators import DataRequired,InputRequired,Length,EqualTo,ValidationError
from models import Credentials,Registration

def DataNotExists(param):
        def _DataNotExists(form,field):
            msg = 'msg'
            if param=='Account number':
                msg = Registration.query.filter_by(account_number=field.data).first()
            if param == 'CIF number':
                msg = Registration.query.filter_by(cif_number=field.data).first()
            
            if param == 'Username':
                msg = Credentials.query.filter_by(username=field.data).first()
            if msg:
                raise ValidationError(param+" Already exists!")
        return _DataNotExists


class SignupForm(Form):
    accno = StringField('Account Number',validators=[DataRequired(),DataNotExists('Account number')])
    cifno = StringField('CIF Number',validators=[DataRequired(),DataNotExists('CIF number')])
    branchcode = StringField('Branch code',validators=[DataRequired()])
    country = SelectField('Country',validators=[DataRequired()], choices=['India','Pakistan'])
    phone = StringField('Phone Number',validators=[DataRequired()])
    facility = SelectField('Facility Required',validators=[DataRequired()],choices=['Full Transaction Rights','Limited Transaction Rights','View Rights'])
    # recaptcha = RecaptchaField('recaptcha')
    submit = SubmitField('Register')


class OTPForm(Form):
    otp = PasswordField('Enter the one time password(OTP)',validators=[DataRequired()])
    submit = SubmitField('Confirm')
    resend = SubmitField('Click here to resend the OTP')

class ATMForm(Form):
    atm = RadioField('atm',choices=[("yes",'I have my ATM card(Online registration without branch visit)'), ("no","I don't have my ATM card(Activation by branch only)")],validators=[InputRequired()])
    submit = SubmitField('Submit')

class UserForm(Form):
    username = StringField('Enter new username',validators=[DataRequired('Please enter username'),Length(min=6,max=20,message="Enter valid username"),DataNotExists('Username')])
    password = PasswordField('Enter new Login Password',validators=[DataRequired('Please enter password'),Length(min=6,max=20,message="Password must be 6 characters or more")])
    confirm_password = PasswordField('Confirm New Login Password',validators=[DataRequired(message='Please enter password'),EqualTo('password', message='Both password fields must be equal!')])
    checkbox = BooleanField('I accept the Terms and Conditions',validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')

def ValidPassword(other):
    def _ValidPassword(form,field):
        username = form[other].data
        user = Credentials.query.filter_by(username = username).first()        
        if user is not None and not user.check_password(field.data):
            raise ValidationError("Wrong Password")
    return _ValidPassword

class PancardForm(Form):
    username = StringField()
    password = PasswordField('Enter password',validators=[DataRequired("Please enter your password."),ValidPassword(other='username')])
    submit = SubmitField('Submit')
         

class EnterPanForm(Form):
    pan = StringField('PAN',validators=[DataRequired("Please enter your PAN number.")])
    repan = PasswordField('Re-enter PAN',validators=[DataRequired("Please re-enter your PAN number."),EqualTo('pan', message='Both pan number fields must be equal!')])
    submit = SubmitField('Submit')



        
