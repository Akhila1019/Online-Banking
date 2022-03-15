from flask_wtf import Form,RecaptchaField
from wtforms import StringField,SubmitField,SelectField,RadioField,BooleanField,PasswordField
from wtforms.validators import DataRequired,InputRequired,Length,EqualTo

class SignupForm(Form):
    accno = StringField('Account Number',validators=[DataRequired()])
    cifno = StringField('CIF Number',validators=[DataRequired()])
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
    username = StringField('Enter new username',validators=[DataRequired('Please enter username'),Length(min=6,max=20,message="Enter valid username")])
    password = PasswordField('Enter new Login Password',validators=[DataRequired('Please enter password'),Length(min=6,max=20,message="Password must be 6 characters or more")])
    confirm_password = PasswordField('Confirm New Login Password',validators=[DataRequired(message='Please enter password'),EqualTo('password', message='Both password fields must be equal!')])
    checkbox = BooleanField('I accept the Terms and Conditions',validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')

class PancardForm(Form):
    password = PasswordField('Enter password',validators=[DataRequired("Please enter your password.")])
    submit = SubmitField('Submit')
