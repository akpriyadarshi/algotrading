'''
              STEPS
- get ltp of spot using ltpData() method
- Calculate ATM strike with help of spot
- Get token, symbol of CE Strike
- Get token, symbol of PE Strike
- place SELL order for CE and PE

'''

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


# In[18]:


obj=SmartConnect(api_key=apiKey)
token=pyotp.TOTP(totp).now()

data = obj.generateSession(userName,password,token)


refreshToken= data['data']['refreshToken']

#print("refresh token: "+refreshToken)

feedToken=obj.getfeedToken()
#print("feed token: "+feedToken)

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
#print(userProfile)


# In[19]:


obj.position()


# In[27]:


import pandas as pd
import requests
import numpy as np
import math

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})


# In[28]:


list(token_df)


# In[29]:


token_df[token_df["symbol"] == "BANKNIFTY"]


# In[30]:


LTP=obj.ltpData("NSE","BANKNIFTY","26009")


# In[33]:


ltp = LTP['data']['ltp']
ltp


# In[53]:


ATMstrike1 = math.floor(ltp/100)*100
ATMstrike1


# In[54]:


ATMstrike2 = math.ceil(ltp/100)*100
ATMstrike2


# In[55]:


if ltp-ATMstrike1 <= ATMstrike2-ltp:
    ATMstrike = ATMstrike1
else:
    ATMstrike = ATMstrike2
    


# In[56]:


ATMstrike


# In[64]:


def place_order(token,symbol,quantity,buy_sell,price):
    try:
        orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": symbol,
        "symboltoken": token,
        "transactiontype": buy_sell,
        "exchange": "NFO",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
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


# In[65]:


def getTokenInfo (df, exch_seg, instrumenttype,symbol,strike_price,pe_ce):
    #df = credentials.TOKEN_MAP
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])


# In[66]:


ce_strike = getTokenInfo(token_df,'NFO','OPTIDX','BANKNIFTY',ATMstrike,'CE').iloc[0]
ce_strike


# In[67]:


pe_strike = getTokenInfo(token_df,'NFO','OPTIDX','BANKNIFTY',ATMstrike,'PE').iloc[0]
pe_strike


# In[68]:


place_order(ce_strike['token'],ce_strike['symbol'],ce_strike['lotsize'],'SELL',0)


# In[69]:


place_order(pe_strike['token'],pe_strike['symbol'],pe_strike['lotsize'],'SELL',0)


# In[ ]:

