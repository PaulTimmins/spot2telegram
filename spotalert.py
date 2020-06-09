#!/usr/bin/python3
import sys
import json
import urllib.request
import pymysql.cursors
connection = pymysql.connect(host='0.0.0.0', user='user', passwd='pw', db='spot', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

apikey = "telegram bot api key here"

def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')

#insertsql = "insert ignore into trackingdata (id,messengerId,feed,messagetype,custommessage,dateTime,unixTime,latitude,longitude) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

cursor = connection.cursor()
updater = connection.cursor()

cursor.execute("select tgchannel,latitude,longitude from trackingdata left join telegram on trackingdata.feed = telegram.feed where processed='N' and locationexpires <= unix_timestamp(now()) group by tgchannel order by dateTime asc")
while True:
  result = cursor.fetchone()
  if result == None:
    break
  bs = urllib.request.urlopen("https://api.telegram.org/bot"+apikey+"/sendLocation?chat_id="+str(result['tgchannel'])+"&latitude="+str(result['latitude'])+"&longitude="+str(result['longitude'])+"&live_period=86400")
  line = bs.read()
  mydata = json.loads(line.decode("utf-8"))
  print(line)
  updater.execute("update telegram set livelocation="+str(mydata['result']['message_id'])+",locationexpires=unix_timestamp(now())+86399 where tgchannel="+str(result['tgchannel']))

connection.commit()

cursor.execute("select * from trackingdata left join telegram on trackingdata.feed = telegram.feed where processed='N' order by unixtime asc")

while True:
  result = cursor.fetchone()
  if result == None:
    break
  feed = result['feed']
  #if result['locationexpires'] > 
  print(feed+" "+result['messagetype']+" "+str(result['tgchannel'])+" ID: "+str(result['id'])+"\n")
  if result['messagetype'] == 'UNLIMITED-TRACK':
    try:
      print("https://api.telegram.org/bot"+apikey+"/editMessageLiveLocation?chat_id="+str(result['tgchannel'])+"&message_id="+str(result['liveLocation'])+"&latitude="+str(result['latitude'])+"&longitude="+str(result['longitude']))
      bs = urllib.request.urlopen("https://api.telegram.org/bot"+apikey+"/editMessageLiveLocation?chat_id="+str(result['tgchannel'])+"&message_id="+str(result['liveLocation'])+"&latitude="+str(result['latitude'])+"&longitude="+str(result['longitude']))
    except:
      print("Telegram update failed")
  else:
    bs = urllib.request.urlopen("https://api.telegram.org/bot"+apikey+"/sendMessage?chat_id="+str(result['tgchannel'])+"&text="+result['messagetype']+"%20pressed%20latitude="+str(result['latitude'])+"%20longitude="+str(result['longitude']))
  line = bs.read() 
  print(line)
  updater.execute("update trackingdata set processed='Y' where id="+str(result['id']))
connection.commit()

