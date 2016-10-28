#!/usr/bin/python 
import requests
from bs4 import BeautifulSoup as bs4
#from bs4 import BeautifulSoup#
#from urllib2 import urlopen
#from datetime import datetime
import csv
#import sys
import os
import gmail
import time
import string
import smtplib
import email
import pickle


#Read write functions
def write_results(link_list):
    with open('links.p','wb') as f:
        pickle.dump(link_list,f)

def read_results():
  data = pickle.load(open('links.p', 'rb'))
  return data

#add email to send from here, use a junk one
gm = gmail.GMail('email@google.com', '123456789')
gm.connect()



# This will remove weird characters that people put in titles like ****!***!!!
use_chars = string.ascii_letters + ''.join([str(i) for i in range(10)]) + ' '

link_list = []  # We'll store the data here
link_list_send = []  # This is a list of links to be sent
send_list = []  # This is what will actually be sent in the email

# Define our URL and a query we want to post
base_url = 'http://sfbay.craigslist.org/search/eby/apa/'
find_url = 'http://sfbay.craigslist.org'
link_list = read_results()

print link_list
print "\n"



zip1 = ['94607']


# Careful with this...too many queries == your IP gets banned temporarily
for zips in zip1:
    url = base_url + '?max_price=1600&postal='+zips+'&search_distance=2'
    resp = requests.get(url)
    txt = bs4(resp.text, 'html.parser')
    apts = txt.findAll(attrs={'class': "row"})
    
    # We're just going to pull the title and link
    for apt in apts:
        price = str(apt.find('span', {'class': 'price'}).text.strip('$'))
        title = apt.find_all('a', attrs={'class': 'hdrlnk'})[0]
        name = ''.join([i for i in title.text if i in use_chars])
        link = title.attrs['href']
        rlink = link.strip('u/eby/apa/.html')

        if rlink not in link_list and rlink not in link_list_send:
            print('Found new listing')
            link_list_send.append(rlink)
            send_list.append(name +' $'+ price + '  -  ' + find_url+link)

working = True
while working == True:
    # Flush the cache if we've found new entries
    if len(link_list_send) > 0:
        print('Sending mail!')
        msg = '\n'.join(send_list)
        m = email.message.Message()
        m.set_payload(msg)
        gm.send(m, ['iamjacobbjones@gmail.com'])
        link_list.extend(link_list_send)
        link_list += link_list_send
        print link_list
        write_results(link_list)
        link_list_send = []
        send_list = []
    working = False






