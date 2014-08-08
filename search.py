import re
import json
import requests


class search:



    def run():
        
        data = requests.get("http://boards.4chan.org/g/catalog").text
        match = re.match(".*var catalog = (?P<catalog>\{.*\});.*", data)

        if not match:
            print("Couldn't scrape catalog")
            exit(1)

        catalog = json.loads(match.group('catalog'))
        liste=[]
        liste1=[]
        running = True
        i=0
        while running:
            
                try:
                    filtertext = ("desktop thread")
                    for number, thread in catalog['threads'].items():
                        id1, sub, teaser = thread['lr'], thread['sub'], thread['teaser']
                        if filtertext in sub.lower():
                            i+=1
                            liste.append(teaser)
                            liste1.append(number)
                            
                            #print(liste[0])
                            #return(teaser.encode('utf-8'))
                            #running = False
                            if i ==1:
                                return(liste), (liste1)

                except KeyboardInterrupt:
                    
                    running = False


#for i in range(2):
#    print(search.run()[i])
#    print("-------------------------------------------------------------")
#print("http://boards.4chan.org/g/thread/"+  +search.run()[0])
liste,id1 = search.run()
#print(liste+id1)
#print("http://boards.4chan.org/g/thread/"+ id1[0]['id'] +search.run()[0]) 
#str = "Id: " + liste([1]['id'])
liste_s=liste+id1

print("http://boards.4chan.org/g/thread/"+ liste_s[1]) 
#print(liste_s[1])
