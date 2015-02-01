import urllib.request
import requests
import json

class Backup:
    def __init__(self, url):
        self.url = url
    def backup(self):
        req_url = self.url
        response = requests.get(req_url)
        obj = response.json() 
        print(json.dumps(obj,sort_keys=True, indent=4, separators=(',', ': ')))
        
    def send(self):
        return requests.post(
              "https://api.mailgun.net/v2/sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org/messages",
              auth=("api", "key-fd78805af31e5a60d8ef0fe9587e2fdd"),
              data={"from": "Mailgun Sandbox <postmaster@sandbox3b110172ed844490b95b97eb9ef9c178.mailgun.org>",
                  "to": "ArvinH <arvin0731@gmail.com>",
                  "subject": "Hello ArvinH",
                  "text": "Congratulations ArvinH, you just sent an email with Mailgun!  You are truly awesome!  You can see a record of this email in your logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this sandbox server.  Next, you should add your own domain so you can send 10,000 emails/month for free."})
        
def main():
   b = Backup('https://slack.com/api/channels.list?token=xoxp-3273763636-3508525695-3580135383-bd3aa9&pretty=1')
   b.backup()



if __name__ == '__main__':
    main()
