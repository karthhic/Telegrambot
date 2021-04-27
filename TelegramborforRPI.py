# This is a sample Python script.
# -*- coding: UTF8 -*-

import requests
import datetime
import os
from time import sleep
import json
from datetime import datetime, date
import configparser
import random
from colorrgb import *
import time
randomColor = (random.randrange(20,255),random.randrange(20,255),random.randrange(20,255))
Enable_PiCamera = False
Enable_senseHat = False

if Enable_senseHat:
    from sense_hat import SenseHat
    sense = SenseHat()
    print("SenseHat is enabled")
else:
    print("SenseHat is disabled")

if Enable_PiCamera:
    from picamera import PiCamera
    print("Pi camera is enabled")
else:
    print("Pi camera disabled")


def pathCheck(path):
    if os.path.exists(path):
        print("Path exists")
    else:
        os.system("mkdir "+path)

def messagedisplay(message, times,color,strip):
    for i in range (0,times):
        sense.show_message(message.strip(strip), text_colour= color , scroll_speed=0.09)
    


class BotHandler:
    def __init__(self, bot_token):
        self.token = bot_token
        self.api_url = "https://api.telegram.org/bot{}/".format(bot_token)


    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, image_path, image_caption=""):
        camera.start_preview()
        sleep(5)
        camera.capture(image_path)
        camera.stop_preview()
        data = {"chat_id": chat_id, "caption": image_caption}
        method = 'sendPhoto'
        with open(image_path, "rb") as image_file:
            resp = requests.post(self.api_url + method, data=data, files={"photo": image_file})
        return resp

    def save_image(self, file_id):
        # print(file_id)
        params = {"file_id": file_id}
        method = "getFile"
        resp = requests.get(self.api_url + method, params)
        contents = (resp.content).decode('utf-8')
        j = json.loads(contents)
        resp = requests.get("https://api.telegram.org/file/bot{}".format(self.token) + "/" + j["result"]["file_path"])
        # print(resp)
        file = open(j["result"]["file_path"], "wb")
        file.write(resp.content)
        file.close()
    
    def save_video(self, file_id):
        # print(file_id)
        params = {"file_id": file_id}
        method = "getFile"
        resp = requests.get(self.api_url + method, params)
        contents = (resp.content).decode('utf-8')
        j = json.loads(contents)
        resp = requests.get("https://api.telegram.org/file/bot{}".format(self.token) + "/" + j["result"]["file_path"])
        # print(resp)
        file = open(j["result"]["file_path"], "wb")
        file.write(resp.content)
        file.close()
    
    def save_document(self, file_id):
        # print(file_id)
        params = {"file_id": file_id}
        method = "getFile"
        resp = requests.get(self.api_url + method, params)
        contents = (resp.content).decode('utf-8')
        j = json.loads(contents)
        resp = requests.get("https://api.telegram.org/file/bot{}".format(self.token) + "/" + j["result"]["file_path"])
        # print(resp)
        file = open(j["result"]["file_path"], "wb")
        file.write(resp.content)
        file.close()

    def get_first_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None
        return last_update


if Enable_PiCamera:
    camera = PiCamera()
now = datetime.now()
today = date.today()
parser = configparser.ConfigParser()
parser.read('config.ini')
token = parser.get('telegrambot', 'token')  # Token of your bot
karkommbot = BotHandler(token)  # Your bot's name
photolocation = parser.get('telegrambot', 'imagename')
loggerlocation = parser.get('telegrambot', 'imagelocation')
timeoftheday = ["Good Morning ", "Good Afternoon ", "Good Evening ", "Go sleep "]
pathCheck("videos")
pathCheck("photos")
pathCheck("documents")

def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates = karkommbot.get_updates(new_offset)
        if len(all_updates) > 0:
            for current_update in all_updates:
                print("-----------------")
                print(current_update)
                print("-----------------")
                first_update_id = current_update['update_id']

                if 'text' not in current_update['message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                current_time = now.strftime("%H:%M:%S")
                current_hour = now.strftime("%H")
                date = today.strftime("%d/%m/%Y")
                log_value = date + ", " + current_time + ", " + first_chat_name + ", " + str(
                    first_chat_id) + ", " + first_chat_text
                print(log_value)
                logfile = open(loggerlocation, "a")
                logfile.write(log_value + "\n")
                logfile.close()

                if 'photo' in current_update['message']:
                    photo_id = current_update['message']['photo'][2]['file_id']
                    karkommbot.save_image(photo_id)
                    karkommbot.send_message(first_chat_id, 'Photo saved successfully')
                if 'video' in current_update['message']:
                    video_id = current_update['message']['video']['file_id']
                    karkommbot.save_video(photo_id)
                    karkommbot.send_message(first_chat_id, 'Video saved successfully')
                if 'document' in current_update['message']:
                    document_id = current_update['message']['document']['file_id']
                    karkommbot.save_document(photo_id)
                    karkommbot.send_message(first_chat_id, 'Video saved successfully')

                if first_chat_text in ('Hi',"hi"):
                    print(current_hour)
                    if int(current_hour) in range(5,12):
                        index = 0
                    elif int(current_hour) in range(12,15):
                        index = 1
                    elif int(current_hour) in range(15, 23):
                        index = 2
                    else:
                        index = 3
                    karkommbot.send_message(first_chat_id, timeoftheday[index] + first_chat_name)
                    #new_offset = first_update_id + 1
                elif first_chat_text in ["photo", "Photo"]:
                    if Enable_PiCamera:
                        karkommbot.send_message(first_chat_id, 'Wait taking photo...')
                        karkommbot.send_photo(first_chat_id, photolocation)
                    else:
                        karkommbot.send_message(first_chat_id, 'Photo option is disabled')
                    #new_offset = first_update_id + 1
                elif first_chat_text.find("msg") != -1 or first_chat_text.find("Msg") != -1:
                    if Enable_senseHat:
                        karkommbot.send_message(first_chat_id, 'Message being displayed')
                        if first_chat_text.find("msg") != -1:
                            messagedisplay(first_chat_text, 3,randomColor,"msg")
                        else:
                            messagedisplay(first_chat_text, 3,randomColor,"Msg")
                    else:
                        karkommbot.send_message(first_chat_id, 'Sensehat Diabled')
                    #new_offset = first_update_id + 1
                elif first_chat_text in ["myid", "Myid"]:
                    karkommbot.send_message(first_chat_id, 'Your chat id is: ' + str(first_chat_id))
                    #new_offset = first_update_id + 1
                else:
                    karkommbot.send_message(first_chat_id,'use commands like myid, photo. you can also send photos and videos ' + first_chat_name)
                    #new_offset = first_update_id + 1
                new_offset = first_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sense.clear((0,0,0))
        exit()


