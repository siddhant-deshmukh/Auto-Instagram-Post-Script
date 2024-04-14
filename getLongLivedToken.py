import os, sys
import requests, json
from dotenv import load_dotenv

# from here get the access token with respected permissions
#  Graph API explorer: https://developers.facebook.com/tools/explorer

# using https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/#get-a-long-lived-user-access-token

# Parameters
API_VERSION = "v18.0"

# Load the environment variables
load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
IG_USER_ID = os.getenv("IG_USER_ID")

# Reading access token
f = open('./token.txt','r+')
ACCESS_TOKEN = f.readline()
# print(access_token)

if(type(APP_ID) != str or type(APP_SECRET) != str or type(ACCESS_TOKEN) != str or len(ACCESS_TOKEN) < 10):
  print(" !!!!!!!!!!!!!!!!!! \tError")
  print("please add .env file in the main.py directory. \nAnd add APP_ID and APP_SECRET fields. \n(get them from App Settings/Basic from your facebook app page.) ")
  print("Also check it token.txt is there with the access token in it")
  sys.exit()

def getToken():
  get_token = "https://graph.facebook.com/" + API_VERSION + "/oauth/access_token" 
  params = { 
    "grant_type": "fb_exchange_token" , 
    "client_id" : APP_ID, 
    "client_secret" : APP_SECRET,
    "fb_exchange_token" : ACCESS_TOKEN,
  }

  res = requests.get(get_token, params=params)
  

  if res.status_code >= 300:
    print("\t\t\t !!!! \t Error while Getting long lived token")
    error = res.json()['error']
    if error is None:
      print("Unknown error", res.json())
    else:
      print("message           :", error['message'])
      print("\nerr", error)
  else:
    extended_token = res.json()['access_token']
    exp_time = res.json()['expires_in']
    print("Extended the token for", exp_time, "sec\t", exp_time/3600, "hours\t", (exp_time/3600)/24 , "days" )

    if extended_token is not None:
      with open("./token.txt", "r+"):
        text = f.read()
        # Move the file position to the beginning
        f.seek(0)
        # Clear the file contents
        f.truncate(0)
        f.write(res.json()['access_token'])
        print("\nsaved token in token.txt")
      return res.json()['access_token']


if __name__ == "__main__":
  getToken()