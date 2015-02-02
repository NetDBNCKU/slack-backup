import json
import requests
import urllib.request

from time import time

class Backup:
    def __init__(self, url_list):
        self.url_list = url_list
        self.user_dict = dict()
        self.channel_list = list()
        self.send_data = list()
        self.mailgun_key = str()

    def get_channels(self):
        req_url = self.url_list
        print(req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        for channel in obj['channels']:
            channel_dict = dict()
            channel_dict['id'] = channel['id']
            channel_dict['name'] = channel['name']
            self.channel_list.append(channel_dict)
#        print (self.channel_list)
#        print(json.dumps(obj,sort_keys=True, indent=4, separators=(',', ': ')))

    def get_users(self):
        req_url = "https://slack.com/api/users.list?token=xoxp-3273763636-3508525695-3580135383-bd3aa9&channel"
        print (req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        for member in obj['members']:
            self.user_dict[member['id']] = member['name']
        self.user_dict['USLACKBOT'] = "slackbot"
#        print (json.dumps(obj, sort_keys=True, indent=4, separators=(',', ": ")))

    def get_message(self):
        for channel in self.channel_list:
            channel_data = dict()
            channel_data['channel_name'] = channel['name']
            channel_data['messages'] = list()
            latest = time()
            while True:
                req_url = "https://slack.com/api/channels.history?token=xoxp-3273763636-3508525695-3580135383-bd3aa9&channel=" + channel['id']\
                                + "&latest=" + str(latest)\
                                + "&count=1000"
                print (req_url)
                response = urllib.request.urlopen(req_url)
                str_response = response.read().decode('utf-8')
                obj = json.loads(str_response)
                for message in obj['messages']:
#                    print (json.dumps(message,sort_keys=True, indent=4, separators=(',', ': ')))
                    message_dict = dict()
                    try:
                        message_dict['user'] = self.user_dict[message['user']]
                    except:
                        if "username" in list(message.keys()):
                            message_dict['user'] = message['username']
                        elif "bot_id" in list(message.keys()):
                            message_dict['user'] = message['bot_id']
                        else:
                            message_dict['user'] = self.user_dict[message['comment']['user']] # Comment post
                    message_dict['text'] = message['text']
                    message_dict['ts'] = message['ts']
                    channel_data['messages'].append(message_dict)
#                print (json.dumps(channel_data['messages'],sort_keys=True, indent=4, separators=(',', ': ')))
                if obj['has_more']:
                    latest = obj['messages'][0]['ts']
                else:
                    break
            self.send_data.append(channel_data)

    def get_mailgun_key(self):
        file = open('mailgun.txt', 'r')
        self.mailgun_key = file.readline()
        file.close()

    def send(self):
        return requests.post(
            "https://api.mailgun.net/v2/sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org/messages",
            auth=("api", self.mailgun_key),
            data={"from": "Mailgun Sandbox <postmaster@sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org>",
                  "to": ["yangpoan@gmail.com"],
                  "subject": "Slack Backup",
                  "text": str(self.send_data)})

def main():
   b = Backup('https://slack.com/api/channels.list?token=xoxp-3273763636-3508525695-3580135383-bd3aa9&pretty=1')
   b.get_channels()
   b.get_users()
   b.get_message()
   b.get_mailgun_key()
   b.send()

if __name__ == '__main__':
    main()
