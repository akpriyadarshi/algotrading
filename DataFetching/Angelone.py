from smartapi import SmartConnect
import time
from datetime import datetime, timedelta
import datetime
import pyotp
import pandas as pd
import requests
import numpy as np
import math


apikey='gmPdFX9J'
username='A1221496'
pwd='0513'  #This is pin not the password of AngelOne
token='CPEXLLRYLGP3YT4553O4OCXB64'


# Create an object of SmartConnect
obj = SmartConnect(api_key=apikey)

def login():
    """
    Function to login and return AUTH and FEED tokens.
    """
    data = obj.generateSession(username, pwd, pyotp.TOTP(token).now())
    refreshToken = data['data']['refreshToken']
    auth_token = data['data']['jwtToken']
    feed_token = obj.getfeedToken()
    return auth_token, feed_token

def historical_data(exchange,token,from_date, to_date,timeperiod):
    """
    Function to fetch historical data and return it as a Pandas DataFrame.
    """
    try:
        historicParam = {
            "exchange": exchange,
            "symboltoken": token,
            "interval": timeperiod,
            "fromdate": from_date, 
            "todate": to_date
        }
        api_response = obj.getCandleData(historicParam)
        data = api_response['data']
        columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(data, columns=columns)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)
        return df
    except Exception as e:
        print("Historic Api failed: {}".format(e))

# Usage Example
auth_token, feed_token = login()

thirty_days_ago = datetime.datetime.now() - timedelta(days=2)
from_date = thirty_days_ago.strftime("%Y-%m-%d %H:%M")
to_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

exchange = "NSE"
#token = 1333
token = 99926009
#timeperiod = "ONE_MINUTE"
timeperiod = "FIVE_MINUTE"
df = historical_data(exchange, token, from_date, to_date,timeperiod)
df2 = historical_data(exchange, token, from_date, to_date, "ONE_MINUTE")
#df2.to_csv('df2_data.txt', sep='\t', index=True)
#print(df)
#df.to_csv('data.txt', sep='\t', index=True)

#################################

## Calculate 5EMA on 5 min candle
primary_ema_value = 46197 # At 3:25 PM Closing 1 Feb 2024
ema_previous = primary_ema_value
multiplier = 0.3333
d = '2024-02-02 09:15:00'
dt = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
count=5

for i in range(0,75):
    #print("5EMA at ", dt, "is ", (df["Close"][i]-ema_previous)*multiplier+ema_previous)
    #if df["High"][i] < (df["Close"][i]-ema_previous)*multiplier+ema_previous:
        #print("BUYING ALERT CANDLE AT", dt )
    if df["Low"][i] > (df["Close"][i]-ema_previous)*multiplier+ema_previous:
        print("SELLING ALERT CANDLE AT", dt )
        ## For now we are treating one minute closing as live data for triggering trade, logic would be changed for realtime data
        for j in range(0,5):
            if df2["Close"][count+j] < df["Low"][i]:
                print("Selling Triggered at", df2["Close"][count+j])
                break

    dt = dt+timedelta(minutes=5)
    ema_previous = (df["Close"][i]-ema_previous)*multiplier+ema_previous
    count = count+5

    

#######################################
    
## Fetching Options data

