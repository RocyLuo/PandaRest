
def code_filter(code_str):
    pass

def set_case_var():
    pass

def remove_case_var():
    pass

def set_module_var():
    pass

def remove_module_var():
    pass

def set_project_var():
    pass

def remove_project_var():
    pass

def user_function(r,code):
    try:
        code = code.replace('\r\n', ';')
        exec code
    except AssertionError, e:
        print str(e)