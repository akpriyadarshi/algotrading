# pip install smartapi-python
from smartapi import SmartConnect, SmartWebSocket
import time
from datetime import datetime
import datetime
import pyotp
apiKey='gmPdFX9J'
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

############# FETCHING LTP DATA #######################################


def GettingLtpData():
    exchange="NSE"  #Or NFO
    symbol="BANKNIFTY"
    symbolToken="26009"
    LTP=obj.ltpData(exchange,symbol,symbolToken)
    high=LTP["data"]["high"]
    low=LTP["data"]["low"]
    ltp=LTP["data"]["ltp"]
   # print(f"Close")
    print(f"Script:{symbol}, High:{high}, Low:{low}, LTP:{ltp}")
    GettingLtpData()

orderPlaceTime= int(9) *60 + int(30)
timenow=(datetime.datetime.now().hour*60 +datetime.datetime.now().minute)
print("Waiting for 9:30 AM, Current time:{}".format(datetime.datetime.now()))


while timenow<orderPlaceTime:
    time.sleep(0.2)
    timenow=(datetime.datetime.now().hour*60 +datetime.datetime.now().minute)
print("Ready for trading, Current time:{}".format(datetime.datetime.now()))


try:
    GettingLtpData()
except Exception as e:
    raise e



# Getting Strike price near to provided LTP in Fyers:- https://www.youtube.com/watch?v=aM0hDdNH7rY