import socket,time, threading
from search import search
from threading import Thread
from omeglebot import OmegleBot


server = b"irc.freenode.net"
channel = b"#motherfucker" 
botnick = b"HottyBotty" 


def ping():

  ircsock.send(b"PONG :pingis\n")  

#def sendmsg(chan , msg):

#  ircsock.send(b"PRIVMSG "+ chan +b" :"+ msg +b"\n") 

#def sendmsg_(chan , msg):

#  time.sleep(30)
#  ircsock.send(b"PRIVMSG "+ chan +b" :"+ msg +b'\r\n')

def primsend(chan:str,msg:str):

  ircsock.send(b"PRIVMSG %s :%s"+ b'\r\n' % (chan,msg))

#def sendspcmsg(chan , msg):

#  ircsock.send(b"PRIVMSG "+ chan +b" :http://boards.4chan.org/g/thread/"+ msg +b'\n')

def joinchan(chan):
  ircsock.send(b"JOIN "+ chan + b"\n")

#def worker():
#  while True:
#    time.sleep(82800)
#    ircsock.send(b"PRIVMSG" +chan +b"Time to show your desktops to the NASA!11!!"+b"\n")
#    ircsock.send(b"PRIVMSG "+ chan +b" :http://boards.4chan.org/g/thread/"+ bytes(listes[1].encode('utf-8') + b"\n"))

 # print(threading.currentThread().getName(), 'Exiting')

 
def omegle():
  troo = False
  while True:
    if troo == True:
      primsend(channel,OmegleBot().start().decode('utf-8'))
      troo = False
            
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))

ircsock.send(b"USER "+ botnick + b" "+ botnick + b" "+ botnick + b" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n")
ircsock.send(b"NICK "+ botnick + b"\n")

joinchan(channel)

time.sleep(10)
w=Thread(target=omegle)

w.start()
while 1:
  global troo

  liste,id1=search.run()
  listes=liste+id1


  ircmsg = ircsock.recv(2048)
  ircmsg = ircmsg.strip(b'\r\n')
  print(ircmsg)


  #if ircmsg.find(b" :tox kill "+botnick) != 1:
  
   # worker()
   

  if ircmsg.find(b"PING :") != -1:

    ping()


 # if ircmsg.find(b":RICE "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello() 
 #   sendspcmsg(channel,bytes(listes[1].encode('utf-8')))
  
  
  if ircmsg.find(b":tox kill ") != -1:
    troo = True
    primsend(channel,"changed.")


#  if ircmsg.find(b":.chat") != -1:
#    sendmsg_(channel,bytes(OmegleBot().start()).decode('utf-8'))
