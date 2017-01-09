import requests
import re
import json
import time
from ..models import *

TEMP_VARS = {}


def set_local_var(key, value):
    TEMP_VARS[key] = value


def clear_local_var(key):
    del TEMP_VARS[key]


class Request:

    def __init__(self, operation, variables):
        self.header = self._get_string_headers(operation)
        self.method = operation.method
        self.url = operation.url
        self.real_url = operation.url
        self.params = self._get_string_params(operation)
        self.body = self._remove_space(operation.body)
        self.variables = variables
        self.expect_status = operation.expect_status
        self.code = operation.test_code
        self.expected_body = operation.expected_body
        self.drive_data = operation.drive_data
        self.operation = operation


    def _get_string_headers(self, operation):
        return '{'+','.join(['"'+header.key+'":'+header.value+'' for header in operation.headers.all()])+'}'

    def _get_string_params(self, operation):
        return '{' + ','.join(['"' + header.key + '":' + header.value + '' for header in operation.parameters.all()])+'}'

    def _remove_space(self,s):
        if not s is None:
            s = s.replace('\n', '')
            #s = s.replace(' ', '')
        return s

    def replace_variables(self):
        self.header = self.get_variables(self.header)
        self.url = self.get_variables(self.url)
        self.real_url = self.url.replace("'", '')
        self.url = self.real_url

        self.params = self.get_variables(self.params)
        if not (self.body is None or self.body == ''):
            self.body = self.get_variables(self.body)
            print self.body
            self.body = json.loads(self.body)

        if not (self.header is None):
            self.header = self.get_variables(self.header)
            print self.header
            self.header = json.loads(self.header)
        if not (self.params is None or self.params == '{}'):
            self.params = self.get_variables(self.params)
            print self.params
            self.params = json.loads(self.params)
            self.real_url = self.url+self._dict_to_param_str(self.params)

    def _get_function_by_name(self, name):
        print 'function name:'+name;
        print 'real name:'+name[0:name.find('(')]
        code = Function.objects.get(name=name[0:name.find('(')].strip()).code
        code = code.replace('\r\n', ';')
        print code
        return code

    def _exec_func(self, func):
        ret = None
        func.strip()
        code = self._get_function_by_name(func)
        exec code
        exec "ret = " + func
        if isinstance(ret,(str,unicode)):
            ret = '"'+ret+'"'
        return str(ret)

    def get_variables(self, s):
        def find_variable(matched):
            key = matched.group()
            key = key.replace('{', '')
            key = key.replace('}', '')
            if TEMP_VARS.has_key(key):
                ret = TEMP_VARS[key]
                if isinstance(ret, (str,unicode)):
                    ret = '"'+ret+'"'
                else:
                    ret = str(ret)
                print "tempRet"+ret
                return ret
            else:
                for vars in self.variables:
                    for var in vars:
                        if key == var.key:
                            return var.value
            return matched.group()

        def find_function(matched):
            func = matched.group()
            func = func.replace('{%', '')
            func = func.replace('%}', '')
            return self._exec_func(func)

        replaced_vars = re.sub(r'{{[0-9a-zA-Z]*}}', find_variable, s)
        replaced_func = re.sub(r'{%.*?%}', find_function, replaced_vars)
        return replaced_func

    def _dict_to_param_str(self,params):
        result = []
        for k in params.keys():
            result.append(k+"="+str(params[k]))
        return '?'+'&'.join(result)

    def get_request_info(self):
        oper_info = {}
        oper_info["url"] = self.real_url
        oper_info["method"] = self.method
        oper_info["header"] = self.header
        oper_info["body"] = self.body
        return oper_info

    def process_response(self, r):
        if not self.expect_status is None:
            assert self.expect_status == r.status_code, 'http status code is wrong'
        code = self.code.replace('\r\n', ';')
        exec code


    def excute(self, skip):
        """
        :return: [{
                    "operation_info": {
                                         "url": "http://wwww.baidu.com/asd?a=1",
                                         "method": "get"
                                         "header": {"key": "value"}
                                         "body": ""
                                       },
                    "operation_result": {
                                         "status_code": 200
                                         "body": ""
                                         }
                    "assert_result" : "Pass"
                    "assert_info" : "str(e)"
                 },......
                 ]
        """
        result = {}
        result['operation_info'] = self.get_request_info()
        result['operation_name'] = self.operation.name
        result["operation_result"] = {}
        self.replace_variables()
        result['operation_info'] = self.get_request_info()
        # try:
        #     self.replace_variables()
        #     result['operation_info'] = self.get_request_info()
        # except Exception, e:
        #     result['assert_result'] = "Error"
        #     result['assert_info'] = str(e)
        #     yield result
        #response = requests.request(self.method, self.url, params=self.params, data=self.body,headers=self.header)
        def send_request():
            try:
                print 'sending request'
                result["operation_result"] = {}
                response = requests.request(self.method, self.url, params=self.params, data=self.body,
                                            headers=self.header)
                print 'Get Response==========:'
                print response.text
                result["operation_result"] = {"status_code": response.status_code, "body": response.text}
                self.process_response(response)

            except AssertionError, e:
                result['assert_result'] = "Fail"
                result['assert_info'] = str(e)
            except Exception, e:
                result['assert_result'] = "Error"
                result['assert_info'] = str(e)
            else:
                result['assert_result'] = "Pass"
                result['assert_info'] = ""

        if skip:
            result["operation_result"] = None
            result['assert_result'] = "Skip"
            result['assert_info'] = ""
            yield result
        else:
            timeout = self.operation.wait_timeout
            period = self.operation.wait_period
            if timeout > 0 and period > 0:
                pass_result = False
                while timeout > 0 and not pass_result:
                    timeout -= period
                    time.sleep(period)
                    send_request()
                    if result['assert_result'] == "Pass":
                        pass_result = True
                    yield result
            else:
                send_request()
                yield result



