import socket
# from en2ar import en2ar
# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
from deep_translator import (GoogleTranslator)
# anzahl_iteration = 0
# Replace <CHANNEL_NAME> with the name of the Twitch channel you want to retrieve chat messages from. Be sure it's in small letter!
# channel_name = 'brittt'  
channel_name = input("Enter the name of the Twitch channel whose chat you want to access: ").lower()
chat_language = input("Enter the chat language: ").lower()
myusername = 'sharatye'
my_oauth_token = '4csmm85vwecklxgxsts9npswxqjf4d'

def TwitchConnect(channel_name, myusername, my_oauth_token):
    # Connect to the Twitch chat server
    sock = socket.create_connection(('irc.chat.twitch.tv', 6667))

    # Log in to the server
    sock.send(f'PASS oauth:{my_oauth_token}\r\n'.encode())
    sock.send(f'NICK {myusername}\r\n'.encode())

    # Join the channel
    sock.send(f'JOIN #{channel_name}\r\n'.encode())
    return sock

def queryOnce(sock, chat_language):
    # Continuously read data from the socket
    try:
        while True:
            data = sock.recv(1024).decode()
            if data.startswith('PING'):
                sock.send('PONG\r\n'.encode())
            elif 'PRIVMSG' in data:
                username = data.split('!')[0][1:]
                message = str(data.split(':')[2][:-1])
                print(f'{username}: {message}')
                en2ar(username, message, chat_language)
            # anzahl_iteration += anzahl_iteration
    except KeyboardInterrupt:
        # restart = (input("Enter 0 to restart loop: "))
        # pass
        queryRepeatedly()
    print('You have exited the chat')

def queryRepeatedly():
    mode = (input("Enter 0 to restart Chat. Enter 1 if you wanna Change Channel name. Enter 2 to change chat language: "))
    if mode=='0':
        sock = TwitchConnect(channel_name, myusername, my_oauth_token)
        queryOnce(sock, chat_language)
    elif mode=='1':
        mode = (input("Enter the Channel name: "))
        sock = TwitchConnect(mode, myusername, my_oauth_token)
        queryOnce(sock, chat_language)
    elif mode=='2':
        mode = (input("Enter the Chat Language(e.g en or english): "))
        sock = TwitchConnect(channel_name, myusername, my_oauth_token)
        queryOnce(sock, chat_language=mode)
    # time.sleep(15)
def en2ar(Msgname, Msgstr, target_language):
    '''
    Parameters:
        Msgstr: Message text
        Msgname: Name of messanger
    '''
    # let's say first you need to translate from auto to german
    my_translator = GoogleTranslator(source='auto', target=f'{target_language}')
    result2 = my_translator.translate(text=Msgstr)
    # print(f"Translation using source = {my_translator.source} and target = {my_translator.target} -> {result2}")
    try:
        result2 = "".join(result2)
    except TypeError:
        pass
    if target_language == 'ar' or target_language == 'arabic':
        reshaped_text = arabic_reshaper.reshape(result2)    # correct its shape
        result2 = get_display(reshaped_text)    
        print(f'{Msgname}: {result2}\n' )
    # if len(result2) == 0 and len(result2) > 0:
    else:
        print(f'{Msgname}: {result2}\n' )
    # return result2

sock = TwitchConnect(channel_name, myusername, my_oauth_token)
queryOnce(sock, chat_language)
