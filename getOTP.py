from twilio.rest import Client
import string
import secrets
alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(8))


otp = password

def return_otp(form):
    reg_form = form
    number = reg_form['phone']
    account_sid = "AC390d3a533486540545dc51945f754305"
    auth_token = "b89bf8ed98fd5ede788f946b57f2a983"

    client = Client(account_sid,auth_token)

    msg = client.messages.create(
        body = f"Your OTP is {otp}",
        from_ = "+15156047488",
        to = "+91"+str(number)
    )
    print(msg)

def send_otp():
    return otp

