#! /usr/bin/env python

# Omegle Bot v0.1
# Copyleft 2012 thefinn93
# Do not run with author permission
# Do not legally obtain this file. It is illegal
# If I catch you with a legal copy of this file I will sue you.
# Dependencies:
# - requests (python-requests.org)

import requests
import sys
import json
import urllib
import random
import time

server = "odo-bucket.omegle.com"

debug_log = open("debug.log","a")
config = {'verbose': open("/dev/null","w")}
headers = {}
headers['Referer'] = 'http://odo-bucket.omegle.com/'
headers['Connection'] = 'keep-alive'
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2'
headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'gzip,deflate,sdch'
headers['Accept-Language'] = 'en-US'
headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'

if debug_log:
    config['verbose'] = debug_log

def debug(msg):
    if debug_log:
        print("DEBUG: " + str(msg))
        debug_log.write(str(msg) + "\n")

def getcookies():
    r = requests.get("http://" + server + "/")
    debug(r.cookies)
    return(r.cookies)

def start():
    r = requests.request("POST", "http://" + server + "/start?rcs=1&spid=", data=b"rcs=1&spid=", headers=headers)
    omegle_id = r.content.strip(b"\"")
    print("Got ID: " + str(omegle_id))
    cookies = getcookies()
    event(omegle_id, cookies)

def send(omegle_id, cookies, msg):
    r = requests.request("POST","http://" + server + "/send", data=b"msg=" + urllib.parse.quote_plus(msg).encode('utf-8') + b"&id=" + omegle_id, headers=headers, cookies=cookies)

    if r.content == b"win":
        print("You: " + msg)
    else:
        print("Error sending message, check the log")
        debug(r.content)

def event(omegle_id, cookies):
    captcha = False
    next = False
    r = requests.request("POST","http://" + server + "/events",data=b"id=" + omegle_id, cookies=cookies, headers=headers)

    parsed = json.loads(r.content.decode('utf-8'))
    for e in parsed:
        if e[0] == "waiting":
            print("Waiting for a connection...")
        elif e[0] == "count":
            print("There are " + str(e[1]) + " people connected to Omegle")
        elif e[0] == "connected":
            print("Connection established!")
            send(omegle_id, cookies, "HI I just want to talk ;_;")
        elif e[0] == "typing":
            print("Stranger is typing...")
        elif e[0] == "stoppedTyping":
            print ("Stranger stopped typing")
        elif e[0] == "gotMessage":
            print("Stranger: " + e[1])
            
            cat=""
            time.sleep(random.randint(1,5))
            i_r=random.randint(1,8)
            if i_r==1:
                cat="that's cute :3"
            elif i_r==2:
                cat="yeah, guess your right.."
            elif i_r==3:
                cat="yeah, tell me something about yourself!!"
            elif i_r==4:
                cat="what's up"
            elif i_r==5:
                cat="me too"
            else:
                time.sleep(random.randint(3,9))
                send(omegle_id, cookies, "I really have to tell you something...")
                time.sleep(random.randint(3,9))
                cat="I love you."

            send(omegle_id, cookies, cat)
           

        elif e[0] == "strangerDisconnected":
            print("Stranger Disconnected")
            next = True
        elif e[0] == "suggestSpyee":
            print ("Omegle thinks you should be a spy. Fuck omegle.")
        elif e[0] == "recaptchaRequired":
            print("Omegle think's you're a bot (now where would it get a silly idea like that?). Fuckin omegle. Recaptcha code: " + e[1])
            captcha = True

        if next:
            print("Reconnecting...")
            start()
        elif not captcha:
             event(omegle_id, cookies)
    

start()

