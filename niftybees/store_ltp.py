from smartapi import SmartConnect
import time
from datetime import datetime
import datetime
import pyotp
import pandas as pd
import requests
import numpy as np
import math


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



url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})

#######################



LTP_niftybees=obj.ltpData("NSE","NIFTYBEES-EQ","10576")
LTP_nifty=obj.ltpData("NSE","NIFTY","26000")
price = LTP_nifty['data']['ltp']
price = int(price)
f = open("/home/knoldus/Algotrading/niftybees/ltp.txt", "r+") 
  
# absolute file positioning
f.seek(0) 
  
# to erase all data 
f.truncate() 
f.close()

f = open("/home/knoldus/Algotrading/niftybees/ltp.txt", "a")
f.write(str(price))
f.close()
#print(LTP_niftybees['data']['ltp'])




#print(list(token_df))
#print(token_df[token_df['name'] == 'NIFTY'])
