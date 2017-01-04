# coding=utf-8
import json

data1 = "{a:1,b:2}"
data2 = '{"a":1,"b":2}'
data3 = '{}'
#json.loads(data1)
print json.loads(data3)


def test(var):
    return var+100
funcStr = "rest = test(100)"

exec funcStr
print rest

