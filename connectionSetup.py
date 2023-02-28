from smartapi import SmartConnect  
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
print(userProfile)

###########################
# https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json  get token and symbols of instruments 
