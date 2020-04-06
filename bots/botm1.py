import sys, os
from json import JSONDecodeError

filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok
parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} browser: {browser_path}')
redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)
client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)
user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print('-----------------------')
class_channel_id = "109ab13498c64fd5911a42be1076ea6b"
my_channel_id = "819cd772643a4cb990245c585c32a930"
channel_to_join_leave = "e00a1405fc5a4dc0980fa3c6dfed5989"
member_to_invite_and_remove = "xiaoluep@uci.edu"
my_email = "weihuanfu@outlook.com"

stop = False
while not stop:
    answer1 = answer2 = ""
    while answer1 not in {"1", "2", "3"}:
        answer1 = input("choose one of the followings: \n"
                        "1. do something with chat messages\n"
                        "2. do something with chat channels\n"
                        "3. end session\n")
    # chat messages test
    if answer1 == "1":
        while answer2 not in {"1", "2", "3", "4", "5"}:
            answer2 = input("what do you want to do with your chat messages?\n"
                            "1. list all messages in the channel on a specific date\n"
                            "2. send a chat message\n"
                            "3. update a message\n"
                            "4. delete a message\n"
                            "5. end session\n")

        # list all messages on a date
        if answer2 == "1":
            select_date = input("type in date, for example: 2020-4-6\n")
            data = client.chat_messages.list(to_channel=my_channel_id, date=select_date, user_id="me")
            messages = data.json().get("messages")
            for message in messages:
                print(message)
            answer1 = answer2 = ""

        # send a message
        elif answer2 == "2":
            message = input("Enter your message: ")
            client.chat_messages.post(to_channel=my_channel_id, message=message)
            answer1 = ""

        # update a message
        elif answer2 == "3":
            select_date = input("Type in date on which you want to change your message, for example: 2020-4-6:\n")
            data = client.chat_messages.list(to_channel=my_channel_id, date=select_date, user_id="me")
            messages = data.json().get("messages")
            print("Here are all the messages on " + select_date + "\n")
            for message in messages:
                print(message)
            message_id = input("Copy paste the message id you want to change: ")
            edited_message = input("Enter your edited message: ")
            data = client.chat_messages.put(message=edited_message, message_id=message_id, to_channel=my_channel_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Message successfully updated-----\n")
            answer1 = answer2 = ""

        # delete a message
        elif answer2 == "4":
            select_date = input("Type in date on which you want to delete your message, for example: 2020-4-6\n")
            data = client.chat_messages.list(to_channel=my_channel_id, date=select_date, user_id="me")
            messages = data.json().get("messages")
            print("Here are all the messages on " + select_date + "\n")
            for message in messages:
                print(message)
            message_id = input("Copy paste the message id you want to delete: ")
            data = client.chat_messages.delete(message_id=message_id, to_channel=my_channel_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Message successfully deleted-----\n")
            answer1 = answer2 = ""

        # end session
        elif answer2 == "5":
            answer1 = answer2 = ""
            break

    # chat channels test
    elif answer1 == "2":
        answer2 = ""
        while answer2 not in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"}:
            answer2 = input("Choose one of the following instructions: \n"
                            "1. List all channels\n"
                            "2. Create a channel\n"
                            "3. Get a channel\n"
                            "4. Update a channel\n"
                            "5. Delete a channel\n"
                            "6. List channel members\n"
                            "7. Invite Channel Members\n"
                            "8. Join a channel\n"
                            "9. Leave a channel\n"
                            "10. Remove a Member\n"
                            "11. End session\n")

        # list all channels
        if answer2 == "1":
            data = client.chat_channels.list()
            channels = data.json().get("channels")
            for channel in channels:
                print(channel)

        # create a channel
        elif answer2 == "2":
            channel_name = input("Enter channel name: ")
            type = 3  # public channel, anyone can search for this channel and join this channel
            email = my_email
            members = [{"email": email}]
            data = client.chat_channels.create(name=channel_name, type=type, members=members)
            print(json.loads(data.content))

        # get a channel
        elif answer2 == "3":
            temp_channel_id = my_channel_id
            data = client.chat_channels.get(channel_id=temp_channel_id)
            print(json.loads(data.content))

        # update a channel name
        elif answer2 == "4":
            print("Here is a list of all channels you have: ")
            data = client.chat_channels.list()
            channels = data.json().get("channels")
            for channel in channels:
                print(channel)
            temp_channel_id = input("Enter channel id that you want to change name (use new created channel for test): ")
            name = input("\nEnter new name of this channel: ")
            data = client.chat_channels.update(channel_id=temp_channel_id, name=name)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Channel name successfully changed-----\n")

        # delete a channel
        elif answer2 == "5":
            print("Here is a list of all channels you have: ")
            data = client.chat_channels.list()
            channels = data.json().get("channels")
            for channel in channels:
                print(channel)
            temp_channel_id = input("\nEnter channel id that you want to delete (use new created channel id): ")
            data = client.chat_channels.delete(channel_id=temp_channel_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Channel successfully deleted-----\n")

        # list channel members
        elif answer2 == "6":
            temp_channel_id = class_channel_id
            data = client.chat_channels.list_members(channel_id=temp_channel_id)
            members = data.json().get("members")
            for member in members:
                print(member)

        # invite channel members
        elif answer2 == "7":
            temp_channel_id = my_channel_id
            member = member_to_invite_and_remove
            members = [{"email": member}]
            data = client.chat_channels.invite(channel_id=temp_channel_id, members=members)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Member successfully invited-----\n")

        # join a channel
        elif answer2 == "8":
            temp_channel_id = channel_to_join_leave
            data = client.chat_channels.join(channel_id=temp_channel_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----You successfully joined the channel-----\n")

        # leave a channel
        elif answer2 == "9":
            temp_channel_id = channel_to_join_leave
            data = client.chat_channels.leave(channel_id=temp_channel_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----You successfully left the channel-----\n")

        # remove a member
        elif answer2 == "10":
            temp_channel_id = my_channel_id
            member_id = member_to_invite_and_remove
            data = client.chat_channels.remove_member(channel_id=temp_channel_id, member_id=member_id)
            try:
                print(json.loads(data.content))
            except JSONDecodeError:
                print("-----Member was successfully removed from this channel-----\n")

        # end session
        elif answer2 == "11":
            break
        answer1 = answer2 = ""

    elif answer1 == "3":
        stop = True
