# import web 
import os, sys
import requests, json
from dotenv import load_dotenv

# Parameters
API_VERSION = "v18.0"

# Load the environment variables
load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
IG_USER_ID = os.getenv("IG_USER_ID")

# Reading access token
f = open('./token.txt','r')
ACCESS_TOKEN = f.readline()
# print(access_token)

if(type(APP_ID) != str or type(APP_SECRET) != str or type(ACCESS_TOKEN) != str or len(ACCESS_TOKEN) < 10):
  print(" !!!!!!!!!!!!!!!!!! \tError")
  print("please add .env file in the main.py directory. \nAnd add APP_ID and APP_SECRET fields. \n(get them from App Settings/Basic from your facebook app page.) ")
  print("Also check it token.txt is there with the access token in it")
  sys.exit()

# custom error message for some special subcodes https://developers.facebook.com/docs/instagram-api/reference/error-codes
error_subcodes = {
  2207020: "Runnning the script again may solve the problem. \n Because the container code has been expired for some reason.",
  2207042: "Daily publishing limit has been reached checkout : \b https://developers.facebook.com/docs/instagram-api/guides/content-publishing/#rate-limit",
  2207006: "Check permission or token once",
  2207052: "Check the image url. It should be properly hosted. Keep this in mind https://support.exclaimer.com/hc/en-gb/articles/4445816657309-How-to-host-images-using-Google-Drive ",
  2207005: "Possible because of permission or token error. \n also check if the url is correct \nKeep this in mind https://support.exclaimer.com/hc/en-gb/articles/4445816657309-How-to-host-images-using-Google-Drive",
  2207009: "Problem with image resolution https://help.instagram.com/1631821640426723"
}

# graph = GraphAPI()

def create_container(img_url, caption=""):

  # posting the image
  create_container_params = { "image_url" : img_url, "caption" : caption, "access_token" : ACCESS_TOKEN }
  create_container_img_url = "https://graph.facebook.com/" + API_VERSION + "/" + IG_USER_ID + "/media" 

  res = requests.post(create_container_img_url, params=create_container_params)

  if(res.status_code == 200):
    container_data = json.loads(res.text)
    creation_id = container_data['id']
    return creation_id
  else:
    print("\t\t\t !!!! \t Error while Creating container                     ")
    error = res.json()['error']
    if error is None:
      print("Unknown error", res.json())
    else:
      print("err", error)
      if('error_user_title' in error):
        print("error title       :" , error['error_user_title'])
      print("message           :", error['message'])
      if('error_user_msg' in error):
        print("how to solve error:", error['error_user_msg'])
      if('error_subcode' in error and  error['error_subcode'] in error_subcodes):
        print("\n\n", error_subcodes[error['error_subcode']])
    return

def publish_container(creation_id):
  publish_container_url = "https://graph.facebook.com/" + API_VERSION + "/" + IG_USER_ID + "/media_publish" 
  params = { "creation_id" :  creation_id, "access_token" : ACCESS_TOKEN }
  res = requests.post(publish_container_url, params=params)
  print("\nresponse publish container : \n", res.text, "\n\n")
  if res.status_code != 200:
    print("\t\t\t !!!! \t Error while Publishing container                     ")
    error = res.json()['error']
    if error is None:
      print("Unknown error", res.json())
    else:
      # print("err", error)
      print("error title       :" , error['error_user_title'])
      print("message           :", error['message'])
      print("how to solve error:", error['error_user_msg'])
      print("\n\n", error_subcodes[error['error_subcode']])
  else:
    print("Published the image with Instagram Media ID", res.json()['id'])
  
def convert_drive_url(google_drive_url):
  # Image From google drive
  # image must be public (Anyone With the Link) and get the unique image id(unique-img-id)
  # https://drive.google.com/file/d/{unique-img-id}/view?usp=sharing
  # https://drive.google.com/uc?id={unique-img-id}
  uniqueImgId = google_drive_url.split('/')[5]
  return "https://drive.google.com/uc?id=" + uniqueImgId      #image should hosted on a public server e.g. drive, dropbox

if __name__ == "__main__":
  google_drive_url = "https://drive.google.com/file/d/1BNp116-5zI23Mhx_pbZHD9HslxweFW2M/view?usp=sharing" 
  caption = "Cute little monkeys!"

  img_url = convert_drive_url(google_drive_url)
  creation_id = create_container(img_url,caption)
  if creation_id is not None:
    publish_container(creation_id) 