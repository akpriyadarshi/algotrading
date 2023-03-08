from smartapi import SmartConnect, SmartWebSocket
import time
from datetime import datetime
import datetime
import pyotp


# In[17]:


apiKey='gmPdFX9J'
userName='A1221496'
password='0513'  #This is pin not the password of AngelOne
totp='CPEXLLRYLGP3YT4553O4OCXB64'

obj=SmartConnect(api_key=apiKey)
token=pyotp.TOTP(totp).now()

data = obj.generateSession(userName,password,token)


refreshToken= data['data']['refreshToken']

#print("refresh token: "+refreshToken)

feedToken=obj.getfeedToken()
#print("feed token: "+feedToken)

#fetch User Profile
userProfile= obj.getProfile(refreshToken)

import pandas as pd
import requests
import numpy as np
import math

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})

#######################
LTP=obj.ltpData("NSE","NIFTYBEES-EQ","10576")

print(LTP['data']['ltp'])
print(LTP['data']['open'])
print(LTP['data']['close'])
print(LTP['data']['low'])

#############################################
def place_order(token,symbol,quantity,buy_sell,price):
    try:
        orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol,
        "symboltoken": token,
        "transactiontype": buy_sell,
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "DELIVERY",
        "duration": "DAY",
        "price": price,
        "squareoff": "0",
        "stoploss": "0",
        "quantity": quantity
        }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))





print("pnl is: ", obj.position()['data'][0]['pnl'])
#place_order('10576','NIFTYBEES-EQ',1,'BUY',0)
