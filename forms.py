from flask_wtf import Form,RecaptchaField
from wtforms import StringField,SubmitField,SelectField,RadioField,BooleanField,PasswordField,DateField
from wtforms.validators import DataRequired,InputRequired,Length,EqualTo,ValidationError
from models import Credentials,Registration,RequestPancard,cheq
from getOTP import *
from werkzeug.security import generate_password_hash,check_password_hash


accno = 'Account Number'
acctype = 'Account Type'
countries = [ "--Select Country--","Afganistan",
                  "Albania",
                   "Algeria",
                   "American Samoa",
                   "Andorra",
                   "Angola",
                   "Anguilla",
                   "Antigua & Barbuda",
                   "Argentina",
                   "Armenia",
                   "Aruba",
                   "Australia",
                   "Austria",
                   "Azerbaijan",
                   "Bahamas",
                   "Bahrain",
                   "Bangladesh",
                   "Barbados",
                   "Belarus",
                   "Belgium",
                   "Belize",
                   "Benin",
                   "Bermuda",
                   "Bhutan",
                   "Bolivia",
                   "Bonaire",
                   "Bosnia & Herzegovina",
                   "Botswana",
                   "Brazil",
                   "British Indian Ocean Ter",
                   "Brunei",
                   "Bulgaria",
                   "Burkina Faso",
                   "Burundi",
                   "Cambodia",
                   "Cameroon",
                   "Canada",
                   "Canary Islands",
                   "Cape Verde",
                   "Cayman Islands",
                   "Central African Republic",
                   "Chad",
                   "Channel Islands",
                   "Chile",
                   "China",
                   "Christmas Island",
                   "Cocos Island",
                   "Colombia",
                   "Comoros",
                   "Congo",
                   "Cook Islands",
                   "Costa Rica",
                   "Cote DIvoire",
                   "Croatia",
                   "Cuba",
                   "Curaco",
                   "Cyprus",
                   "Czech Republic",
                   "Denmark",
                   "Djibouti",
                   "Dominica",
                   "Dominican Republic",
                   "East Timor",
                   "Ecuador",
                   "Egypt",
                   "El Salvador",
                   "Equatorial Guinea",
                   "Eritrea",
                   "Estonia",
                   "Ethiopia",
                   "Falkland Islands",
                   "Faroe Islands",
                   "Fiji",
                   "Finland",
                   "France",
                   "French Guiana",
                   "French Polynesia",
                   "French Southern Ter",
                   "Gabon",
                   "Gambia",
                   "Georgia",
                   "Germany",
                   "Ghana",
                   "Gibraltar",
                   "Great Britain",
                   "Greece",
                   "Greenland",
                   "Grenada",
                   "Guadeloupe",
                   "Guam",
                   "Guatemala",
                   "Guinea",
                   "Guyana",
                   "Haiti",
                   "Hawaii",
                   "Honduras",
                   "Hong Kong",
                   "Hungary",
                   "Iceland",
                   "Indonesia",
                   "India",
                   "Iran",
                   "Iraq",
                   "Ireland",
                   "Isle of Man",
                   "Israel",
                   "Italy",
                   "Jamaica",
                   "Japan",
                   "Jordan",
                   "Kazakhstan",
                   "Kenya",
                   "Kiribati",
                   "Korea North",
                   "Korea Sout",
                   "Kuwait",
                   "Kyrgyzstan",
                   "Laos",
                   "Latvia",
                   "Lebanon",
                   "Lesotho",
                   "Liberia",
                   "Libya",
                   "Liechtenstein",
                   "Lithuania",
                   "Luxembourg",
                   "Macau",
                   "Macedonia",
                   "Madagascar",
                   "Malaysia",
                   "Malawi",
                   "Maldives",
                   "Mali",
                   "Malta",
                   "Marshall Islands",
                   "Martinique",
                   "Mauritania",
                   "Mauritius",
                   "Mayotte",
                   "Mexico",
                   "Midway Islands",
                   "Moldova",
                   "Monaco",
                   "Mongolia",
                   "Montserrat",
                   "Morocco",
                   "Mozambique",
                   "Myanmar",
                   "Nambia",
                   "Nauru",
                   "Nepal",
                   "Netherland Antilles",
                   "Netherlands",
                   "Nevis",
                   "New Caledonia",
                   "New Zealand",
                   "Nicaragua",
                   "Niger",
                   "Nigeria",
                   "Niue",
                   "Norfolk Island",
                   "Norway",
                   "Oman",
                   "Pakistan",
                   "Palau Island",
                   "Palestine",
                   "Panama",
                   "Papua New Guinea",
                   "Paraguay",
                   "Peru",
                   "Phillipines",
                   "Pitcairn Island",
                   "Poland",
                   "Portugal",
                   "Puerto Rico",
                   "Qatar",
                   "Republic of Montenegro",
                   "Republic of Serbia",
                   "Reunion",
                   "Romania",
                   "Russia",
                   "Rwanda",
                   "St Barthelemy",
                   "St Eustatius",
                   "St Helena",
                   "St Kitts-Nevis",
                   "St Lucia",
                   "St Maarten",
                   "St Pierre & Miquelon",
                   "St Vincent & Grenadines",
                   "Saipan",
                   "Samoa",
                   "Samoa American",
                   "San Marino",
                   "Sao Tome & Principe",
                   "Saudi Arabia",
                   "Senegal",
                   "Seychelles",
                   "Sierra Leone",
                   "Singapore",
                   "Slovakia",
                   "Slovenia",
                   "Solomon Islands",
                   "Somalia",
                   "South Africa",
                   "Spain",
                   "Sri Lanka",
                   "Sudan",
                   "Suriname",
                   "Swaziland",
                   "Sweden",
                   "Switzerland",
                   "Syria",
                   "Tahiti",
                   "Taiwan",
                   "Tajikistan",
                   "Tanzania",
                   "Thailand",
                   "Togo",
                   "Tokelau",
                   "Tonga",
                   "Trinidad & Tobago",
                   "Tunisia",
                   "Turkey",
                   "Turkmenistan",
                   "Turks & Caicos Is",
                   "Tuvalu",
                   "Uganda",
                   "United Kingdom",
                   "Ukraine",
                   "United Arab Erimates",
                   "United States of America",
                   "Uraguay",
                   "Uzbekistan",
                   "Vanuatu",
                   "Vatican City State",
                   "Venezuela",
                   "Vietnam",
                   "Virgin Islands (Brit)",
                   "Virgin Islands (USA)",
                   "Wake Island",
                   "Wallis & Futana Is",
                   "Yemen",
                   "Zaire",
                   "Zambia",
                   "Zimbabwe",]
options = ['--Select Type of Account--','Savings Account','Current Account']
# ***************************************************************************
def data_not_exists(param):
    def _data_not_exists(form,field):
        msg = 'msg'
        if param==accno:
            msg = Registration.query.filter_by(account_number=field.data).first()
        if param == 'CIF number':
            msg = Registration.query.filter_by(cif_number=field.data).first()
        
        if param == 'Username':
            msg = Credentials.query.filter_by(username=field.data).first()
        if msg:
            raise ValidationError(param +" Already exists!")
    return _data_not_exists

class SignupForm(Form):
    accno = StringField(accno,validators=[DataRequired('Please enter Account Number'),Length(min=9,max=18,message="Enter valid Account number"),data_not_exists(accno)])
    cifno = StringField('CIF Number',validators=[DataRequired('Please enter CIF Number'),data_not_exists('CIF number'),Length(min=9,max=11,message="Enter valid CIF number")])
    branchcode = StringField('Branch code',validators=[DataRequired('Please enter branch code'),Length(min=4,max=6,message="Enter valid branch code")])
    country = SelectField('Country',validators=[DataRequired('Please select a country')], choices=countries)
    phone = StringField('Phone Number',validators=[DataRequired('Please enter phone number')])
    facility = SelectField('Facility Required',validators=[DataRequired('Please select facility required')],choices=['Full Transaction Rights','Limited Transaction Rights','View Rights'])
    submit = SubmitField('Register')

def valid_otp():
    def _valid_otp(form,field):
        subotp = form['otp'].data
        smsotp = str(send_otp())
        print(smsotp)
        if smsotp!= subotp:
            raise ValidationError("Wrong OTP")
    return _valid_otp

class OTPForm(Form):
    otp = PasswordField('Enter the one time password(OTP)',validators=[DataRequired(),valid_otp()])
    submit = SubmitField('Confirm')

class ATMForm(Form):
    atm = RadioField('atm',choices=[("yes",'I have my ATM card(Online registration without branch visit)'), ("no","I don't have my ATM card(Activation by branch only)")],validators=[InputRequired()])
    submit = SubmitField('Submit')

# ************************************************************************
class UserForm(Form):
    username = StringField('Enter new username',validators=[DataRequired('Please enter username'),Length(min=6,max=20,message="Enter valid username"),data_not_exists('Username')])
    password = PasswordField('Enter new Login Password',validators=[DataRequired('Please enter password'),Length(min=6,max=20,message="Password must be 6 characters or more")])
    confirm_password = PasswordField('Confirm New Login Password',validators=[DataRequired(message='Please enter password'),EqualTo('password', message='Both password fields must be equal!')])
    checkbox = BooleanField('I accept the Terms and Conditions',validators=[DataRequired()])
    submit = SubmitField('Submit')

def valid_password(other):
    def _valid_password(form,field):
        username = form[other].data
        user = Credentials.query.filter_by(username = username).first()
        if user is not None and not user.check_password(field.data):
            raise ValidationError("Wrong Password")
    return _valid_password

# *********************************************************************

class PancardForm(Form):
    username = StringField()
    password = PasswordField('Enter password',validators=[DataRequired("Please enter your password."),valid_password(other='username')])
    submit = SubmitField('Submit')
         
class EnterPanForm(Form):
    username = StringField()
    pan = StringField('PAN',validators=[DataRequired("Please enter your PAN number.")])
    repan = PasswordField('Re-enter PAN',validators=[DataRequired("Please re-enter your PAN number."),EqualTo('pan', message='Both pan number fields must be equal!')])
    submit = SubmitField('Submit')

#  ****************************************************************
def valid_user(other):
    def _valid_user(form,field):
        username = form[other].data
        user = Credentials.query.filter_by(username = username).first()
        if user is None:
            raise ValidationError("User with provided details doesn't exist")
        if user is not None and not user.check_password(field.data):
            raise ValidationError("Wrong Password. Try again")
    return _valid_user

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    password = PasswordField('Enter password',validators=[DataRequired("Please enter your password."),valid_user(other='username')])
    submit = SubmitField('Login')

# *************************************************************** 

class EnterGstForm(Form):
    pan = StringField('Enter Pan',validators=[DataRequired("Please enter your pan number.")])
    gst = PasswordField('Enter GST number',validators=[DataRequired("Please enter your GST number.")])
    submit = SubmitField('Submit')

# ***************************************************************** 
def valid_old_password(other):
    def _valid_old_password(form,field):
        username = form[other].data
        user = Credentials.query.filter_by(username = username).first()
        if user is None or not user.check_password(field.data):
            raise ValidationError("Wrong Password")
    return _valid_old_password

class  ChangePwdForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter username.")])
    old = PasswordField('Old Password', validators=[DataRequired("Please enter old password."),valid_old_password(other='username')])
    new1 = PasswordField('New Password', validators=[DataRequired("Please enter new password."),Length(min=6,max=20, message="password must be minimum 8 characters")])
    new2 = PasswordField('Retype New Password',validators=[DataRequired("Please re-enter new password."),EqualTo('new1',message="New Password and confirm password must be same")])
    submit=SubmitField('Submit')

# *******************************************************************
def valid_account():
    def _valid_account(form,field):
        accno = field.data
        user = Registration.query.filter_by(account_number = accno).first()
        if user is None:
            raise ValidationError("Account number does not exist")
    return _valid_account

def valid_cheque():
    def _valid_cheque(form,field):
        cheqno = field.data
        user = cheq.query.filter_by(cheqnum = cheqno).first()
        if user is None:
            raise ValidationError("Cheque number does not exist")
    return _valid_cheque
    
class ChequeForm(Form):
    ac=StringField(accno, validators=[DataRequired("Please enter your Account Number."),valid_account()])
    thr = StringField('Maximum Theshold Limit for each Cheque', validators=[DataRequired("Please enter your email address.")])
    ncheq=SelectField('Number of Cheque Books', choices=[('1', '1'), ('2', '2')])
    nleaf=SelectField('Number of Cheque Leaves', choices=[('1', '10'), ('2', '20'),('3','25'),('4','50')])
    submit = SubmitField("Submit")

class StopchequeForm(Form):
    SCheqNum = StringField('Start Cheque Number',validators=[DataRequired('Start Cheque Number is required'),valid_cheque()])
    ECheqNum = StringField('End Cheque Number',validators=[DataRequired('End Cheque Number is reqired'),valid_cheque()])
    Reason = StringField('Reason :',validators=[DataRequired('Reason is required')])
    acctype = SelectField(acctype,validators=[DataRequired()], choices=options)
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

# ********************************************************** 

class ForgotForm(Form):
    accno = StringField(accno,validators=[DataRequired('Please enter Account number'),valid_account()])
    phone = StringField('Phone Number',validators=[DataRequired('Please enter phone number')])
    submit = SubmitField('Submit')

class NewpwdForm(Form):
    pwd = PasswordField('New Password',validators=[DataRequired()])
    submit = SubmitField('Update')
   
# *********************************************************

class RequestForm(Form):
    ano = StringField(accno,validators=[DataRequired('Account Number is Required'),valid_account()])
    bname= StringField('Benificiary Name',validators=[DataRequired('Benificiary name is required.')])
    amou=StringField('DD Amount',validators=[DataRequired('Amount is Required')])
    place=StringField('Place to be drawn at',validators=[DataRequired('Place to be Drawn is required')])
    submit = SubmitField('Request')




# ****************************************************************

class ACForm(Form):
    acctype = SelectField(acctype,validators=[DataRequired()], choices=options)
    period = DateField('Select Period',validators=[DataRequired()])
    submit = SubmitField('Show')
    back = SubmitField('Back')

class StatusForm(Form):
    cheqnum = StringField('Cheque Number',validators=[DataRequired('Cheque Number is required'),valid_cheque()])
    acctype = SelectField(acctype,validators=[DataRequired()], choices=options)
    view = SubmitField('View')

class ViewAcBalForm(Form):
    ac=StringField(accno, validators=[DataRequired("Please enter your Account Number."),valid_account()])
    submit = SubmitField("View Balance")

class AmountMonthForm(Form):
    accno = StringField(accno,validators=[DataRequired()])
    acctype = SelectField(acctype,validators=[DataRequired()], choices=options)
    period1 = DateField('From',validators=[DataRequired()])
    period2 = DateField('To',validators=[DataRequired()])
    submit = SubmitField('Show')
    back = SubmitField('Back')

class QuickTransferForm(Form):
    accnum = StringField('Account Number',validators=[DataRequired(),valid_account()])
    amountq= StringField('Balance',validators=[DataRequired()])
    benname=StringField('Benificiary Name',validators=[DataRequired()])
    benaccno=StringField('Beneficiary account number',validators=[DataRequired()])
    rebenaccno=StringField('Re enter Beneficiary account number',validators=[DataRequired(),EqualTo('benaccno', message='Both Beneficiary account number fields must be equal!')])
    purpose=StringField('Purpose',validators=[DataRequired()])
    submit = SubmitField('Proceed')
    

class FundsTransferForm(Form):
    amt = StringField('Amount',validators=[DataRequired()])
    purpose = StringField('Purpose',validators=[DataRequired()])
    acctype = SelectField(acctype,validators=[DataRequired()], choices=options)
    accno = StringField('Select Account Number')
    submit = SubmitField('Proceed')

class FdForm(Form):
    accno = StringField('Account Number :',validators=[DataRequired(),valid_account()])
    download = SubmitField('Download Fixed Deposit Summary')

class VerifyForm(Form):
    confirm = SubmitField('Download Fixed Deposit Summary')

# ********************************************************************
class HomeForm(Form):
    logout = SubmitField('Log Out')