########################################################################
# ay18t2-smt203-lesson-04-01-telegram
# references:
# 	http://docs.python-requests.org/en/v0.6.1/api/#requests.models.Response
# 	https://core.telegram.org/bots/api
#   https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
# objectives:
#   in this exercise, you will learn how to use the Telegram API to
#   - CRUD text messages (send, read, update, delete msg)
#   - send stickers, photos and files via Telegram
########################################################################

import requests, re
import json
import datetime
import time
########################################################################
# global variables
########################################################################

my_token = '' # put your secret Telegram token here
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

########################################################################
# The telegram API supports GET and POST HTTP methods.
# https://core.telegram.org/bots/api#available-methods
# The HTTP URLs for each method looks like this:
# https://api.telegram.org/bot{token}/{method_name}.
# The following defines the URLs for each method that we will use.
########################################################################

# if you are not sure how each of these look like, you can print them
url_getMe = '{}getme'.format(url_base)
url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)
url_editMsgText = '{}editMessageText'.format(url_base)
url_delMsg = '{}deleteMessage'.format(url_base)

url_sendPhoto = '{}sendPhoto'.format(url_base)
url_sendDoc = '{}sendDocument'.format(url_base)
url_sendSticker = '{}sendSticker'.format(url_base)

# here, we define common functions that we can use
def print_pretty_json(url,params):
    r = requests.get(url = url, params = params)
    json_object = r.json()
    # print(json.dumps(json_object, indent=2, sort_keys=True))
    return json.dumps(json_object, indent=2, sort_keys=True)

def reqjson(url,params):
    r = requests.get(url = url, params = params)
    return r.json()

def get_url():
    try:
        contents = requests.get('http://206.189.146.224:5000/serverstatus')
        return contents
    except Exception as e:
        return str(e)

def send_welcome_msg():

    # write your code here
    params = {}
    user_list = []
    r = reqjson(url_getUpdates,params)
    r = r['result'][0]
    chat_id = r['message']['from']['id']

    text = get_url()
    params = {'text':text, 'chat_id':chat_id,'format':'json'}
    r2 = reqjson(url_sendMsg,params)

    # your code should end above this line
    return r2

# while True:
#     send_welcome_msg()
while True:
    send_welcome_msg()
    time.sleep(3)
