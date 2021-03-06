"""
    if it is possible, all params and returns would be model objects
    such as [class:`Catalog <model.Model.Catalog>` object,class:`Catalog <model.Model.Catalog>` object,..]
"""
from ..models import *
from Request import Request
from Database import *
from datetime import datetime
import threading


class Runner(threading.Thread):
    def __init__(self, catalog_id, thread_name):
        super(Runner, self).__init__(name=thread_name)
        self.catalog_id = catalog_id
        print 'start running'
        self.catalog = Catalog.objects.get(pk=self.catalog_id)
        self.cases = get_catalog_cases(self.catalog)
        self.project = get_catalog_project(self.catalog)
        self.report = create_report(self.project, self.cases)
        print 'got ' + str(len(self.cases)) + ' cases'

    def run(self):
        """
            :param catalog_id:
            :return: None
            """
        # it is the most complicated core logic function
        # so, get a couple of coffee

        for case in self.cases:
            case_results = []
            skip = False
            path = get_case_path(case)
            variables = get_case_variables(case)
            operations = get_case_operations(case)
            repeat = case.repeat
            print 'start running a case'
            while repeat > 0:
                repeat -= 1
                for operation in operations:
                    if isinstance(operation, RequestOperation):
                        request = Request(operation, variables)
                        for result in request.excute(skip):
                            print str(result)
                            case_results.append(result['assert_result'])
                            if operation.skip_next == 1 and not result["assert_result"] == "Pass":
                                skip = True
                            save_request_operation_log(self.report, path, result)
                    if isinstance(operation, DBOperation):
                        db = Database(operation, variables)
                        for result in db.excute(skip):
                            if operation.skip_next == 1 and not result["assert_result"] == "Pass":
                                skip = True
                            save_db_operation_log(self.report, path, result)
            update_report(self.report, case_results)
        self.report.end_time = datetime.now()
        self.report.status = 'finished'
        self.report.save()


def run(catalog_id):
    """
    :param catalog_id:
    :return: None
    """
    # it is the most complicated core logic function
    # so, get a couple of coffee
    print 'start running'
    catalog = Catalog.objects.get(pk=catalog_id)
    cases = get_catalog_cases(catalog)
    project = get_catalog_project(catalog)
    report = create_report(project, cases)
    print 'got '+str(len(cases))+' cases'
    for case in cases:
        skip = False
        path = get_case_path(case)
        variables = get_case_variables(case)
        operations = get_case_operations(case)
        repeat = case.repeat
        print 'start running a case'
        while repeat > 0:
            repeat -= 1
            for operation in operations:
                if isinstance(operation, RequestOperation):
                    request = Request(operation, variables)
                    for result in request.excute(skip):
                        print str(result)
                        if operation.skip_next == 1 and not result["assert_result"] == "Pass":
                            skip = True
                        save_request_operation_log(report, path, result)
                if isinstance(operation, DBOperation):
                    db = Database(operation,variables)
                    for result in db.excute(skip):
                        if operation.skip_next == 1 and not result["assert_result"] == "Pass":
                            skip = True
                        save_db_operation_log(report, path, result)


def get_catalog_cases(catalog):
    """
    :param: catalog
    :return: [case1,case2,case3...]
    """
    result = []

    def recur_catalog(catalog):
        if catalog.type == 'Case':
            result.append(catalog)
        children = Catalog.objects.all().filter(parent__id=catalog.id).exclude(type='Template').order_by('priority')
        for child in children:
            recur_catalog(child)

    recur_catalog(catalog)
    return result


def get_case_path(case):
    """
    :param case:
    :return:[catalog(case),catalog(module),catalog(project)]
    """
    result = []

    def recur_catalog_up(catalog):
        result.append(catalog)

        if not catalog.parent_id is None:
            parent = Catalog.objects.get(pk=catalog.parent.id)
            recur_catalog_up(parent)

    recur_catalog_up(case)
    return result


def get_catalog_project(catalog):
    """
    :param catalog:
    :return: project
    """

    return get_case_path(catalog)[-1]


def get_case_variables(case):
    """
    :param: case
    :return: [[variable1,variable2],[variable1],[variable1,variable2]]
    """
    result = []
    catalogs = get_case_path(case)
    for catalog in catalogs:
        result.append(Variable.objects.all().filter(catalog__id=catalog.id))
    return result


def get_case_operations(case):
    """
    :param case:
    :return: [request1,request2,db1,db2,request3,...] order by priority
    """
    result = []
    result.extend(RequestOperation.objects.filter(catalog__id=case.id))
    result.extend(DBOperation.objects.filter(catalog__id=case.id))
    result = sorted(result, key=lambda model: model.priority)
    return result


def save_request_operation_log(report, path, request_result):
    """
    :param report:
    :param path:
    :param request_result:
    :return: Operation_log
    """
    operation_log = OperationLog()
    operation_log.report = report
    operation_log.type = 'request'
    operation_log.case_name = path[0].name
    operation_log.module_name = path[1].name
    operation_log.name = request_result["operation_name"]
    operation_log.operation_info = request_result["operation_info"]
    operation_log.operation_result = request_result["operation_result"]
    operation_log.assert_result = request_result["assert_result"]
    operation_log.assert_info = request_result["assert_info"]
    operation_log.save()
    return operation_log


def save_db_operation_log(report, path, db_result):
    """
    :param report:
    :param path:
    :param db_result:
    :return:
    """
    return


def create_report(project, cases):
    """
    :param project:
    :param cases:
    :return: report
    """
    report = Report()
    report.start_time = datetime.now()
    report.project_id = project.id
    report.project_name = project.name
    report.case_total = len(cases)
    report.case_pass = 0
    report.case_fail = 0
    report.case_error = 0
    report.case_skip = 0
    report.save()
    return report

def get_case_result(case_results):
    if 'Error' in case_results:
        return 'Error'
    elif 'Fail' in case_results:
        return 'Fail'
    else:
        return 'Pass'

def update_report(report, case_results):
    case_result = get_case_result(case_results)
    if case_result == 'Pass':
        report.case_pass +=1
    if case_result == 'Fail':
        report.case_fail += 1
    if case_result == 'Error':
        report.case_error += 1
    report.save()


def update_report_result(report):
    """
    :param report:
    :return:
    """
    return report