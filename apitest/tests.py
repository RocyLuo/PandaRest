# coding=utf-8
import json

data1 = "{a:1,b:2}"
data2 = '{"a":1,"b":2,"c":"ab"}'
data3 = '{"param1":"qweqwe","param2":12323}'
#json.loads(data1)
data = json.loads(data3)

ff = '1.23'
print float(ff)


a = "fu123"
print isinstance(data["param1"],(str,unicode))
print type(data["param1"])

c = []
c.append([3,2,3,4,])
print c





