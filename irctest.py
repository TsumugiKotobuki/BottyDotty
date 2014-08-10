import socket,time, threading
from search import search
from threading import Thread
from omeglebot import OmegleBot


server = b"irc.freenode.net"
channel = b"###cookies" 
botnick = b"HottyBotty" 


def ping():

  ircsock.send(b"PONG :pingis\n")  

def sendmsg(chan , msg):

  ircsock.send(b"PRIVMSG "+ chan +b" :"+ msg +b"\n") 

def sendspcmsg(chan , msg):

  ircsock.send(b"PRIVMSG "+ chan +b" :http://boards.4chan.org/g/thread/"+ msg +b"\n")



def joinchan(chan):
  ircsock.send(b"JOIN "+ chan + b"\n")

def worker():
  while True:
    time.sleep(82800)
    ircsock.send(b"PRIVMSG" +chan +b"Time to show your desktops to the NASA!11!!"+b"\n")
    ircsock.send(b"PRIVMSG "+ chan +b" :http://boards.4chan.org/g/thread/"+ bytes(listes[1].encode('utf-8') + b"\n"))

 # print(threading.currentThread().getName(), 'Exiting')

                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))

ircsock.send(b"USER "+ botnick + b" "+ botnick + b" "+ botnick + b" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n")
ircsock.send(b"NICK "+ botnick + b"\n")

joinchan(channel)

time.sleep(10)
#w=Thread(target=worker)

#w.start()
while 1:

  liste,id1=search.run()
  listes=liste+id1


  ircmsg = ircsock.recv(2048)
  ircmsg = ircmsg.strip(b'\n\r')
  print(ircmsg)


  #if ircmsg.find(b" :tox kill "+botnick) != 1:
  
   # worker()
   

  if ircmsg.find(b"PING :") != -1:

    ping()


  if ircmsg.find(b":RICE "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello() 
    sendspcmsg(channel,bytes(listes[1].encode('utf-8')))
  
  
  if ircmsg.find(b":tox kill "+ botnick) != -1:
    sendmsg(channel,b".insult yukarin")


  if ircmsg.find(b":.chat") != -1:
    sendmsg(channel,bytes(OmegleBot().start()))
