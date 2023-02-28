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

############################################
exchange="NSE"  #Or NFO
symbol="BANKNIFTY"
symbolToken="26009"
interval="ONE_MINUTE"
fromdate= "2023-01-17 14:52"
todate= "2023-01-17 14:53"
LTP=obj.ltpData(exchange,symbol,symbolToken)
high=LTP["data"]["high"]
low=LTP["data"]["low"]
ltp=LTP["data"]["ltp"]
close=LTP["data"]["close"]
# print(f"Close")
print(LTP)


####################################################################
    
def OHLCHistory(symbol,token,interval,fdate,todate):
    try:
        historicParam={
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "interval": interval,
            "fromdate": fdate,
            "todate": todate
        } 
        history=obj.getCandleData(historicParam)['data']  ###
        print(history)
        history=pd.DataFrame(history)

        history=history.rename(
            columns={0: "Datetime", 1: "open", 2: "high", 3: "low", 4: "close"}
        )

        history['Datetime']=pd.to_datetime(history['Datetime'])
        history=history.set_index('Datetime')
        return history
    except Exception as e:
        print("Historic Api failed: {}".format(e))


# SBIN-EQ, 3045
#minute5data=OHLCHistory("BANKNIFTY","26009","FIVE_MINUTE","2023-01-17 15:00","2023-01-17 15:05")
minute5data=OHLCHistory("SBIN-EQ","3045","FIVE_MINUTE","2023-01-17 15:00","2023-01-17 15:05")
print("5 minute data:")
my_df=pd.DataFrame(minute5data)
print(my_df)



####################################










