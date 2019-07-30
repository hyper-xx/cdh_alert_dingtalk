import requests
import json
import configparser
import os
import datetime

cfg=configparser.ConfigParser()
cfg.read('config.conf')
cfg.sections()

cm_host=cfg.get('cm','cm_host')
cm_user=cfg.get('cm','cm_user')
cm_passwd=cfg.get('cm','cm_passwd')

dingrobot=cfg.get('alert','dingrobot')
notice=cfg.get('alert','notice')



base_dir = os.getcwd()
countidfile=os.path.join(base_dir,'countid')
f=open(countidfile,'r')
countid=f.readline()
f.close()

def query_request(params):
    data = requests.get(cm_host + params, auth=(cm_user, cm_passwd))
    data = json.loads(data.text)
    return data

def ding_alert(message):
    dingurl = dingrobot
    #atmobile = list(map(str, notice))
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        },
        "at": {
            "atMobiles": notice,
        }
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = json.dumps(data)
    requests.post(dingurl, headers=headers, data=data)


def time_convert(str_time):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(str_time, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return str(localtime)

data=query_request('events?query=alert==true&maxResults=2&resultOffset=0')
totalresults=data['totalResults']

if totalresults > int(countid):
    offset=totalresults-int(countid)
    query_url='events?query=alert==true&maxResults='+str(offset)+'&resultOffset=0'
    alertdata=query_request(query_url)
    f=open(countidfile,'w')
    f.write(str(totalresults))
    f.close()
    #print('timeOccurred: '+alertdata['items'][0]['timeOccurred']+'\n'+'severity: '+alertdata['items'][0]['severity']+'\n'+'values: '+alertdata['items'][0]['attributes'][0]['values'][0]+'\n'+alertdata['items'][0]['attributes'][1]['name']+': '+alertdata['items'][0]['attributes'][1]['values'][0])
    for i in range(int(offset)):
        #print('timeOccurred: ' + time_convert(alertdata['items'][i]['timeOccurred']) + '\n\n' + 'severity: ' + alertdata['items'][i]['severity'] + '\n\n' + 'values: ' + alertdata['items'][i]['attributes'][0]['values'][0] + '\n\n\n\n' +alertdata['items'][i]['attributes'][1]['name'] + ': ' + alertdata['items'][i]['attributes'][1]['values'][0])
        alertmessage='timeOccurred: '+ time_convert(alertdata['items'][i]['timeOccurred'])+'\n\n'+'severity: '+alertdata['items'][i]['severity']+'\n\n'+'values: '+alertdata['items'][i]['attributes'][0]['values'][0]+'\n\n\n\n'+alertdata['items'][i]['attributes'][1]['name']+': '+alertdata['items'][i]['attributes'][1]['values'][0]
        ding_alert(alertmessage)

