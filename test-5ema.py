from smartapi import SmartConnect  
import pyotp
import talib
import numpy
import pandas as pd
import http.client
#import plotly.express as px

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


#####################
try:
        historicParam={
            "exchange": "NSE",
            "tradingsymbol": "BANKNIFTY",
            "symboltoken": "26009",
            "interval": "FIVE_MINUTE",
            "fromdate": "2023-01-17 15:00",
            "todate": "2023-01-17 15:05"
        } 
        history=obj.getCandleData(historicParam)  ###
        print(history)

except Exception as e:
        print("Historic Api failed: {}".format(e))        