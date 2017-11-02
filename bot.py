# bot.py
# The main code for the bot
# Author : Michael Zarate

import bot_config
import bot_utilities
import socket
import re
import time
import threading
from time import sleep


def main():
    # Configure Network
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((bot_config.HOST, bot_config.PORT))
    sock.send("PASS {}\r\n".format(bot_config.PASSWORD).encode("utf-8"))
    sock.send("NICK {}\r\n".format(bot_config.BOTNAME).encode("utf-8"))
    sock.send("JOIN {}\r\n".format(bot_config.CHANNEL).encode("utf-8"))

    chat_msg = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    bot_utilities.chat(sock, "Hi Everyone!! :)")

    threading._start_new_thread(bot_utilities.thread_fill_operator_list, ())

    while True:
        response = sock.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_msg.sub("", response)
            print(response)

            #Custom Commands
            if message.strip() == "!time":
                bot_utilities.chat(sock, "It is currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))
            if message.strip() == "!messages" and bot_utilities.is_operator(username):
                bot_utilities.chat(sock, "Please check out Thorus's git hub stuff at github.com/DRpandaMD")
        sleep(1)


if __name__ == "__main__":
    main()

