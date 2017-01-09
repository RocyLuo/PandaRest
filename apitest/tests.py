# coding=utf-8
import json

data1 = "{a:1,b:2}"
data2 = '{"a":1,"b":2,"c":"ab"}'
data3 = '{   "username": "test",   "signature": "260b315d8cfd23ab2b1f1a098638cf70",   "domains": ["test.video.com"],   "start_time": "2016-09-18 09:50",   "end_time": "2016-09-18 09:55"}'
#json.loads(data1)
data = json.loads(data3)
print data
ff = '1.23'
print float(ff)


c = []
c.append([3,2,3,4,])
print c

from datetime import datetime
print datetime.now()

ttt = ['pass','error','fail']
print 'error' in ttt

user_id = '100001'
access_key = '67678uihqwieh8172gg81h237128h3812h83'
def getSignature(user_id, access_key):
    import hashlib
    import time
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    myHash = hashlib.md5()
    myHash.update(today+user_id+access_key)
    return myHash.hexdigest()

print getSignature(user_id,access_key)



