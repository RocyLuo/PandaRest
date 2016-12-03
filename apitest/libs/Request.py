import requests
import re
import json
from userFunctions import *

class Request:

    def __init__(self, header, method, url, params, body,variables,status=200, code=''):
        self.header = header
        self.method = method
        self.url = url
        self.params = params
        self.body = body
        self.variables = variables
        self.expect_status = status
        self.code = code
        self.real_url = url

    def replace_all(self):
        self.header = self.get_variables(self.header)
        self.url = self.get_variables(self.url)
        self.real_url = self.url
        self.body = self.get_variables(self.body)
        self.params = self.get_variables(self.params)
        if not (self.header is None or self.header == ''):
            self.header = self.get_variables(self.header)
            self.header = json.loads(self.header)
        if not (self.params is None or self.params == ''):
            self.params = self.get_variables(self.params)
            self.params = json.loads(self.params)
            self.real_url = self.url+self._dict_to_param_str(self.params)

    def get_variables(self, s):
        def find_variable(matched):
            key = matched.group()
            key = key.replace('{', '')
            key = key.replace('}', '')
            for var in self.variables:
                if key in var:
                    return var[key]
            return matched.group()

        return re.sub(r'{{[0-9a-zA-Z]*}}', find_variable, s)

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

    def request(self,skip):
        """
        :return: {
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
                 }
        """

        self.replace_all()
        result = {}
        result['operation_info'] = self.get_request_info()

        if skip:
            result["operation_result"] = None
            result['assert_result'] = "Skip"
            result['assert_info'] = ""
            return result

        try:
            response = requests.request(self.method, self.url, params = self.params, data = self.body, headers = self.header)
            result["operation_result"] = {"status_code": response.status_code,"body": response.text}
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

        return result

    def process_response(self, r):
        if not self.expect_status is None:
            assert self.expect_status == r.status_code, 'check status code'
        code = self.code.replace('\r\n', ';')
        exec code



