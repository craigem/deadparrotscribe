#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Dead Parrot Scribe

An IRC note taker for those of us pining for the Fjords.

@author Craige McWhirter (craige@mcwhirter.io)
@copyright Copyright (c) 2014 Craige McWhirter
@License GPLv3
"""

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import socket
import time

# Configure the scribe:
server = "irc.freenode.net" # Server to connect to.
channel = "##DPScribe" # Channel to join.
botnick = "DPScribe" # Give the bot a nick.


def ping():
    '''
    This function will respond to server Pings.
    '''
    ircsock.send("PONG :pingis\n")

def sendmsg(chan, msg):
    '''
    This is the send message function, it simply sends messages to the channel.
    '''
    ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")

def joinchan(chan):
    '''
    This function is used to join channels.
    '''
    ircsock.send("JOIN " + chan + "\n")

def hello():
    '''
    This function responds to a user that inputs "Hello miss"
    '''
    ircsock.send("PRIVMSG " + channel + " :What do you mean \"miss\"?\n")
    time.sleep(3)
    ircsock.send("PRIVMSG " + channel + " :I'm sorry, I have a cold.\n")

def whatsup():
    '''
    This function responds to a user that inputs "What's up $botnic"
    '''
    ircsock.send(
        "PRIVMSG " + channel +
        " :I've had a look 'round the back of the shop, and uh, " +
        "we're right out of parrots.\n")


def getpage(url):
    '''
    Gets a URL from IRC reads it
    '''
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()


def grabtitle():
    '''
    Processes the URL passed from the channel
    '''
    try:
        titlepage = BeautifulSoup(getpage(url[0]))
        for child in titlepage.title:
            sendmsg(channel, "Title: "+ child.encode("utf-8"))
    except urllib2.HTTPError, error:
        print(error)
        dead = str(error)
        sendmsg(
            channel,
            "Oh yes, the, uh, that URL...What's,uh...What's wrong with it?")
        time.sleep(3)
        sendmsg(
            channel,
            "I'll tell you what's wrong with it, my lad. 'E's " +
            dead.split("Error ", 1)[1] +
            ", that's what's wrong with it!")
        time.sleep(3)
        sendmsg(
            channel,
            "No, no, 'e's uh,...he's resting.")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Here we connect to the server using the port 6667
ircsock.connect((server, 6667))
# user authentication
ircsock.send("USER " + botnick + " " + botnick + " " + botnick + " : wat?\n")
# here we actually assign the nick to the bot
ircsock.send("NICK "+ botnick +"\n")

joinchan(channel) # Join the channel using the functions we previously defined

ircmsg = ircsock.recv(2048) # receive data from the server
ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.

while ircmsg.find(channel) == -1:
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.

while 1: # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server

    # Read the channel for URLS and print the title.
    url = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        ircmsg)
    if len(url) > 0:
        grabtitle()

    # If we can find "Hello miss" it will call the function hello()
    if ircmsg.find(":Hello " + "miss") != -1:
        hello()

    # If the server pings us then we've got to respond!
    if ircmsg.find("PING :") != -1:
        ping()

    # If we can find "What's Up $botnick" it will call the function whatsup()
    if ircmsg.find(":What's up " + botnick) != -1:
        whatsup()

# TODO
# Take Notes
# Record them somewhere non-volatile
# Be able to play them back
# Have them sent (email?) to a configurable address.

