from concurrent.futures import ThreadPoolExecutor
import socket,time, threading
from search import search
from threading import Thread
import omeglebot
import concurrent.futures


server = "irc.freenode.net"
channel = "#motherfucker" 
channelb = b"#motherfucker"
botnick = "HottyBotty" 
botnickb = b"HottyBotty"
troo = False

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ping():

  send("PONG :pingis")  


def send(message:str):

  print("sending to server:", message)
  ircsock.send(message.encode() + b'\r\n')


def primsend(chan:str,msg:str):

  send("PRIVMSG %s :%s" % (chan,msg))


def joinchan(chan):
  send("JOIN "+ chan)

#def worker():
#  while True:
#    time.sleep(82800)
#    ircsock.send(b"PRIVMSG" +chan +b"Time to show your desktops to the NASA!11!!"+b"\n")
#    ircsock.send(b"PRIVMSG "+ chan +b" :http://boards.4chan.org/g/thread/"+ bytes(listes[1].encode('utf-8') + b"\n"))

 # print(threading.currentThread().getName(), 'Exiting')

 
def omegle():
  
  obj1 = OmegleBot()
  obj1.start()
  
   
def startloop():
  executor = ThreadPoolExecutor(max_workers=2)
            

  ircsock.connect((server, 6667))

  ircsock.send(b"USER "+ botnickb + b" "+ botnickb + b" "+ botnickb + b" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\r\n")
  send("NICK "+ botnick)

  joinchan(channel)

  time.sleep(10)
#w=Thread(target=omegle)

#w.start()

  while 1:
  
    liste,id1=search.run()
    listes=liste+id1


    ircmsg = ircsock.recv(2048).strip().decode()
    ircmsg = ircmsg.strip('\r\n')
    print(ircmsg.encode('utf-8'))


  #if ircmsg.find(b" :tox kill "+botnick) != 1:
  
   # worker()
   

    if ircmsg.find("PING :") != -1:

      ping()


 # if ircmsg.find(b":RICE "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello() 
 #   sendspcmsg(channel,bytes(listes[1].encode('utf-8')))
  
  
    if ircmsg.find(":tox kill") != -1:
      troo = True
      primsend(channel,"changed.")


    if ircmsg.find(":.chat") != -1:
      executor.submit(omegle)

startloop()
