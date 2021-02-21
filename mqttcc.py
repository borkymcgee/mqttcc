#!/usr/bin/env python3

################## mqttcc - mqtt computer control ######################

import paho.mqtt.client as mqtt
import os
import pynput
from pynput.keyboard import Key, Controller

broker_url = "127.0.0.1" #replace with the IP of your mqtt broker
broker_port = 1883
display_name = "eDP-1" #name of your display for brightness control via xrandr, replace with the result of running "xrandr | grep primary | awk '{print $1}'"
device_name = "MY_COMPUTER" #replace with how you want this device to identify itself
uname ="USERNAME" #replace with your mqtt username
pword ="PASSWORD" #replace with your mqtt password

def on_brightness_message(client, userdata, message):
    os.system("xrandr --output {} --brightness {}".format(display_name, int(message.payload.decode()) / 100))
    print("brightness set to {}%".format(message.payload.decode()))
 
def on_volume_message(client, userdata, message):
    os.system("amixer set Master {}%".format(message.payload.decode()))

def on_application_message(client, userdata, message):
    os.system("wmctrl -a {}".format(message.payload.decode()))

def on_command_message(client, userdata, message):
    os.system(message.payload.decode)
    
def on_key_message(client, userdata, message):
    if message.payload.decode() == "play/pause":
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
    elif message.payload.decode() == "next":
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
    elif message.payload.decode() == "previous":
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
    elif message.payload.decode() == "up":
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif message.payload.decode() == "down":
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif message.payload.decode() == "left":
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif message.payload.decode() == "right":
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif message.payload.decode() == "enter":
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif message.payload.decode() == "space":
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif message.payload.decode() == "backspace":
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)

def on_message(client, userdata, message):
   print("Message Recieved")

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code ", (rc))

client = mqtt.Client(client_id=device_name)
client.on_connect = on_connect
#To Process Every Other Message
client.on_message = on_message
client.username_pw_set(username=uname, password=pword)
client.connect(broker_url, broker_port)
keyboard = Controller()

client.subscribe(device_name + "/brightness", qos=1)
client.subscribe(device_name + "/volume", qos=1)
client.subscribe(device_name + "/application", qos=1)
client.subscribe(device_name + "/key", qos=1)
client.subscribe(device_name + "/command", qos=1)

client.message_callback_add(device_name + "brightness", on_brightness_message)
client.message_callback_add(device_name + "/volume", on_volume_message)
client.message_callback_add(device_name + "/application", on_application_message)
client.message_callback_add(device_name + "/key", on_media_message)
client.message_callback_add(device_name + "/command", on_command_message)

client.loop_forever()
