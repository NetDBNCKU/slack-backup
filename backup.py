import urllib.request
import json

class Backup:
    def __init__(self, url, datasrc):
        self.url = url
    def backup(self):
        req_url = self.url
        print(req_url)
        response = urllib.request.urlopen(req_url)
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        #print(json.dumps(obj,sort_keys=True, indent=4, separators=(',', ': ')))
        
        
def main():
    b = Backup('')
    b.backup()



if __name__ == '__main__':
    main()
