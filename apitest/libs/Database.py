
class Database:

    def __init__(self, operation, variables):
        self.operation = operation
        self.variables = variables

    def excute(self,skip):
        print 'excute_sql:'+str(self.operation)