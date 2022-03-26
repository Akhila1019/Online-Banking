from random import randint
from flask import session
from twilio.rest import Client

otp = randint(100000,999999)

def returnOTP():
    reg_form = session['reg_form']
    number = reg_form['phone']
    account_sid = "AC390d3a533486540545dc51945f754305"
    auth_token = "904b88c315e940f745b23585b3de8035"

    client = Client(account_sid,auth_token)

    msg = client.messages.create(
        body = f"Your OTP is {otp}",
        from_ = "+15156047488",
        to = "+91"+str(number)
    )

def sendOTP():
    return otp

