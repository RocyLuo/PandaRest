# coding=utf-8
import re

s='http://www.baidu.com/{{instance}}/{{a}}{{{{b}}}}'

varss =  [{'a':'C'},{'b':'B','instance':'is-1231'},{'a':'A'}]

def replace(s,variables):

    def find_variable(matched):
        key = matched.group()
        print key
        key = key.replace('{','')
        key = key.replace('}','')
        for var in variables:
            if key in var:
                return var[key]
        return matched.group()


    return re.sub(r'{{[0-9a-zA-Z]*}}',find_variable,s)

action1 = 'assert 1 == 1;a = 1;b = 2;print a;print b'
def user_function(code):
    exec code

user_function(action1)

