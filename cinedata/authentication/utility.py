from twilio.rest import Client

from decouple import config

import random

import string
          
def sending_sms(phone_num,otp):

    account_sid = config('TWILIO_ACC_SID')

    auth_token = config('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
            from_ = '+14452911731',
            to=f'{phone_num}',
            body=f'Your OTP for Verification is : {otp}'
            )
        
def get_otp():

    otp = ''.join(random.choices(string.digits, k=4))

    return otp