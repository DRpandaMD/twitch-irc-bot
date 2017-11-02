# bot_utilities.py
# Utility functions for the twitch bot
# Author: Michael Zarate

import bot_config
import requests
from time import sleep


# Function chat
# Sends a chat message to the server
# Parameters:
# Socket is the socket where the message will get sent to
# Message contains the message


def chat(socket, message):
    socket.send("PRIVMSG #{} :{}\r\n".format(bot_config.CHANNEL, message).encode('utf-8'))

# Function ban
# Bans user from the channel
# Takes socket and a user name as Arguments


def ban(socket, user):
    chat(socket, ".ban {}".format(user))

# Function timeout
# Timeout a user for a period of time
# Takes socket, user and seconds (default is 600)


def timeout(socket, user, seconds=600):
    chat(socket, ".timemout {}".format(user,seconds))


# Function:  thread_fill_operator_list
# Creates a list of operators who can issue commands to the bot
def thread_fill_operator_list():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/thorusmunger/chatters"
            request = requests.get(url)
            json_data = request.json()
            if request.status_code != 502:
                bot_config.operator_list.clear()
                # I want to clean this up
                for person in json_data["chatters"]["moderators"]:
                    bot_config.operator_list[person] = "mod"
                for person in json_data["chatters"]["global_mods"]:
                    bot_config.operator_list[person] = "global_mod"
                for person in json_data["chatters"]["admins"]:
                    bot_config.operator_list[person] = "admins"
                for person in json_data["chatters"]["staff"]:
                    bot_config.operator_list[person] = "staff"
        # I want to narrow down this exception
        except:
            'do nothing'
        sleep(5)


# Function is Operator?
# Finds out if the user is part of the mod, global mods, admin or staff group


def is_operator(user):
    return user in bot_config.operator_list
