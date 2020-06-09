#!/usr/bin/python3
import sys
import json
import urllib.request
import pymysql.cursors
connection = pymysql.connect(host='0.0.0.0', user='user', passwd='pw', db='spot', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')

insertsql = "insert ignore into trackingdata (id,messengerId,feed,messagetype,custommessage,dateTime,unixTime,latitude,longitude) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

cursor = connection.cursor()

cursor.execute("select * from apitotrack where active='Y' and lastseen < date_sub(now(),interval 3 minute)")

while True:
  result = cursor.fetchone()
  if result == None:
    break
  apikey = result['apikey']

  bs = urllib.request.urlopen("https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/"+str(apikey)+"/message.json")

  line = bs.read()
  try:
   pdata = json.loads(line.decode('utf-8'))
  except:
   print(line.decode('utf-8'))

  insertcursor = connection.cursor()
  for rec in pdata['response']['feedMessageResponse']['messages']['message']:
    print(str(rec['id'])+str(rec['messengerId'])+str(apikey)+str(rec['messageType'])+str(rec['messageDetail'])+str(rec['dateTime'])+str(rec['unixTime'])+str(rec['latitude'])+str(rec['longitude'])+"\n")
    insertcursor.execute(insertsql,(str(rec['id']),str(rec['messengerId']),str(apikey),str(rec['messageType']),str(rec['messageDetail']),str(rec['dateTime']),str(rec['unixTime']),str(rec['latitude']),str(rec['longitude'])))
  insertcursor.execute("update apitotrack set lastseen=now() where id=%s", (result['id']))
  connection.commit()

