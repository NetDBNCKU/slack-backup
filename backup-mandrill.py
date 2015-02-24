import json
import requests
import subprocess
import urllib.request
import mandrill

from time import time

class Backup:
    def __init__(self):
        self.token = str()
        self.user_dict = dict()
        self.channel_list = list()
        self.private_channel_list = list()
        self.send_data = list()
        self.mailgun_key = str()
        self.mandrill_key = str()
        self.latestTime = time()
        self.oldest = str()
        self.now_path = str()

    def get_pwd(self):
        self.now_path = subprocess.check_output("pwd", shell=True)
        self.now_path = self.now_path.decode('utf-8')[:-1]
#        print (self.now_path)

    def get_token(self):
        file = open(self.now_path + '/slack_token.txt', 'r')
        self.token = file.readline()[:-1]
        file.close()

    def get_channels(self):
        req_url = "https://slack.com/api/channels.list?token=" + self.token + "&pretty=1"
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

    def get_private_channels(self):
        req_url = "https://slack.com/api/groups.list?token=" + self.token
        print(req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        for private_channel in obj['groups']:
            private_channel_dict = dict()
            private_channel_dict['id'] = private_channel['id']
            private_channel_dict['name'] = private_channel['name']
            self.private_channel_list.append(private_channel_dict)
#        print (self.private_channel_list)
#        print (json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def get_users(self):
        req_url = "https://slack.com/api/users.list?token=" + self.token
        print (req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        for member in obj['members']:
            self.user_dict[member['id']] = member['name']
        self.user_dict['USLACKBOT'] = "slackbot"
#        print (json.dumps(obj, sort_keys=True, indent=4, separators=(',', ": ")))

    def get_message(self):
        self.oldest = self.get_latest_backup_time()
        self.latestTime = time()
        self.set_latest_backup_time()
        for channel in self.channel_list:
            channel_data = dict()
            channel_data['channel_name'] = channel['name']
            channel_data['messages'] = list()
            while True:
                req_url = "https://slack.com/api/channels.history?token=" + self.token\
                                + "&channel=" + channel['id']\
                                + "&oldest=" + str(self.oldest)\
                                + "&latest=" + str(self.latestTime)\
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


    def get_private_message(self):
        self.oldest = "0"
        self.latestTime = time()
        for channel in self.private_channel_list:
            channel_data = dict()
            channel_data['channel_name'] = channel['name']
            channel_data['messages'] = list()
            while True:
                req_url = "https://slack.com/api/groups.history?token=" + self.token\
                                + "&channel=" + channel['id']\
                                + "&oldest=" + str(self.oldest)\
                                + "&latest=" + str(self.latestTime)\
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
#            print (channel_data)
            self.send_data.append(channel_data)

    def set_latest_backup_time(self):
        file = open(self.now_path + '/latest_backup_time.txt','w')
        file.write(str(self.latestTime))
        file.close()

    def get_latest_backup_time(self):
        file = open(self.now_path + '/latest_backup_time.txt','r')
        self.oldest = file.readline()[:-1]
        file.close()
        return self.oldest

    def get_mailgun_key(self):
        file = open(self.now_path + '/mailgun.txt', 'r')
        self.mailgun_key = file.readline()[:-1]
        file.close()

    def get_mandrill_key(self):
        file = open(self.now_path + '/mandrill.txt', 'r')
        self.mandrill_key = file.readline()[:-1]
        file.close()

    def send(self):
        return requests.post(
            "https://api.mailgun.net/v2/sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org/messages",
            auth=("api", self.mailgun_key),
            data={"from": "Mailgun Sandbox <postmaster@sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org>",
                  "to": ["arvin0731@gmail.com","ktchuang@gmail.com","yangpoan@gmail.com"],
                  "subject": "Slack Backup",
                  "text": json.dumps(self.send_data,sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False) })
            #"ktchuang@gmail.com"

    def send_mail(self,template_name, email_to):
        print(self.mandrill_key)
        try:
                mandrill_client = mandrill.Mandrill(self.mandrill_key)
                message = {
                        'to': [],
                        'global_merge_vars': []
                }
                for em in email_to:
                     message['to'].append({'email': em})

                message['global_merge_vars'].append([json.dumps(self.send_data,sort_keys=True, indent=4, separators=(',', ': '))])
                mandrill_client.messages.send(message=message,async=False, ip_pool='Main Pool')


        except mandrill.Error:
    		# Mandrill errors are thrown as exceptions
                print("got some error from mandrill")
                raise



def main():
    b = Backup()
    b.get_pwd()
    b.get_token()
    b.get_channels()
    b.get_users()
    b.get_message()
    b.get_mailgun_key()
    b.send()
#   b.get_mandrill_key()
#   b.send_mail('template-1', ["arvin0731@gmail.com"])

    b_private = Backup()
    b_private.get_pwd()
    b_private.get_token()
    b_private.get_private_channels()
    b_private.get_users()
    b_private.get_private_message()
    b_private.send()
if __name__ == '__main__':
    main()
