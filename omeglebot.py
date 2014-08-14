#!/usr/bin/env python3

# Based on Omegle Bot v0.1, Copyleft 2012 thefinn93
# The way this file was obtained in is illegal in 73 states.

import json
import urllib.request
import urllib.parse
import urllib.error
import random
import time
import requests


class OmegleBot:
    server = "odo-bucket.omegle.com"
    headers = {'Referer': 'http://odo-bucket.omegle.com/', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko)'
                             ' Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2',
               'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': 'application/json',
               'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}

    def __init__(self,ircfunc):
        self._ircfunc = ircfunc
        self._config = {'verbose': open("/dev/null", "w+")}
        self._debug_log = open("debug.log", "a+")
        if self._debug_log:
            self._config['verbose'] = self._debug_log

        self._first_message = True

    def debug(self, msg):
        if self._debug_log:
            print("DEBUG: " + str(msg))
            self._debug_log.write(str(msg) + "\n")

    def getcookies(self):
        r = requests.get("http://" + self.server + "/")
        self.debug(r.cookies)
        return r.cookies

    def start(self):
        self._ircfunc("###cookies","starting...")
        r = requests.request("POST", "http://" + self.server + "/start?rcs=1&spid=",
                             data=b"rcs=1&spid=",
                             headers=self.headers)
        omegle_id = r.content.strip(b"\"")
        print("Got ID: " + str(omegle_id))
        cookies = self.getcookies()
        self.event(omegle_id, cookies)

    def send(self, omegle_id, cookies, msg):
        r = requests.request("POST", "http://" + self.server + "/send",
                             data=b"msg=" + urllib.parse.quote_plus(msg).encode('utf-8') + b"&id=" + omegle_id,
                             headers=self.headers, cookies=cookies)

        if r.content == b"win":
            print("You: " + msg)
        else:
            print("Error sending message, check the log")
            self.debug(r.content)

    def event(self, omegle_id, cookies):
        captcha = False
        again = False
        r = requests.request("POST", "http://" + self.server + "/events", data=b"id=" + omegle_id, cookies=cookies,
                             headers=self.headers)

        parsed = json.loads(r.content.decode('utf-8'))
        for e in parsed:
            if e[0] == "waiting":
                print("Waiting for a connection...")
                self._ircfunc("###cookies","waiting...")
            elif e[0] == "count":
                print("There are " + str(e[1]) + " people connected to Omegle")
                
            elif e[0] == "connected":
                print("Connection established!")
                self._ircfunc("###cookies","connected")
            elif e[0] == "typing":
                print("Stranger is typing...")
                self._ircfunc("###cookies","stranger is typing")

            elif e[0] == "stoppedTyping":
                print("Stranger stopped typing")

            elif e[0] == "gotMessage":
                print("Stranger: " + e[1])
                self._ircfunc("###cookies","Stranger: "+e[1])
                response = self.handle_message(e[1])
                time.sleep(random.randint(1, 5))
                self.send(omegle_id, cookies, response)
                self._ircfunc("###cookies","You:"+response)

            elif e[0] == "strangerDisconnected":
                print("Stranger Disconnected")
                self._ircfunc("###cookies","stranger disconnected")
                self._first_message = True
                again = True

            elif e[0] == "suggestSpyee":
                print("Omegle thinks you should be a spy. Fuck omegle.")

            elif e[0] == "recaptchaRequired":
                print("Omegle think's you're a bot (now where would it get a silly idea like that?)."
                      " Fuckin omegle. Recaptcha code: " + e[1])
                self._ircfunc("###cookies","Captcha")
                captcha = True

            if again:
                print("Reconnecting...")
                self._ircfunc("###cookies","Reconnecting...")
                self.start()
            elif not captcha:
                self.event(omegle_id, cookies)

    # noinspection PyMethodMayBeStatic
    def handle_message(self, message: str) -> str:
        if self._first_message:
            self._first_message = False
            return "Hello! I'll be your psychologist for tonight. What's on your mind?"
        return random.choice(["How does that make you feel?", "Go on...", "Mhm?"])



