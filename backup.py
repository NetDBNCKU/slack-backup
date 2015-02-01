import urllib.request
import json

class Backup:
    def __init__(self, url):
        self.url = url
    def backup(self):
        req_url = self.url
        print(req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        print(json.dumps(obj,sort_keys=True, indent=4, separators=(',', ': ')))
        
        
def main():
   b = Backup('https://slack.com/api/channels.list?token=xoxp-3273763636-3508525695-3580135383-bd3aa9&pretty=1')
   b.backup()



if __name__ == '__main__':
    main()
