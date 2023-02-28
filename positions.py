from smartapi import SmartConnect, SmartWebSocket
import time
from datetime import datetime
import datetime
import pyotp
apiKey='DmUofr3t'
userName='A1221496'
password='0513'  #This is pin not the password of AngelOne
totp='CPEXLLRYLGP3YT4553O4OCXB64'
#pip install pyotp
#pip --no-cache-dir install --upgrade smartapi-python

obj=SmartConnect(api_key=apiKey)
token=pyotp.TOTP(totp).now()

data = obj.generateSession(userName,password,token)


refreshToken= data['data']['refreshToken']

print("refresh token: "+refreshToken)

feedToken=obj.getfeedToken()
print("feed token: "+feedToken)

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
#print(userProfile)

print(obj.position()['data'])
#print(obj.holding())