from django.shortcuts import render
from apitest.models import *

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

def index(request):
    return render(request, 'ui/index.html')


def project_detail(request, pk):
    """
    :param request:
    :param pk:
    :return: result = [
                        {
                            'module':object:Catalog,
                            'vars':object:Variables,
                            'children': [
                                {'case':object:Catalog,
                                'vars':objects:Variables,
                                'operations':object:[RequestOperation,DbOperation]},
                                {'case':object:Catalog,
                                'vars':objects:Variables,
                                'operations':object:[RequestOperation,DbOperation]},
                                ....
                            ]
                        },
                        {
                            'module':object:Catalog,
                            'vars':object:Variables,
                            'children': [
                                {'case':object:Catalog,
                                'vars':objects:Variables,
                                'operations':object:[RequestOperation,DbOperation]},
                                {'case':object:Catalog,
                                'vars':objects:Variables,
                                'operations':object:[RequestOperation,DbOperation]},
                                ....
                            ]
                        },
                        .....
                    ]
    """
    result = []
    template = Catalog.objects.all().filter(type='Template', parent__id=pk)
    project_vars = Variable.objects.all().filter(catalog__id=pk)
    modules = Catalog.objects.all().filter(type='Module', parent__id=pk).order_by('priority')
    for module in modules:
        module_suite = {}
        module_suite['module'] = module
        module_suite['vars'] = Variable.objects.all().filter(catalog__id=module.id)
        module_suite['children'] = []
        cases = Catalog.objects.all().filter(type='Case', parent__id=pk)
        for case in cases:
            child = {}
            child['case'].append(case)
            child['vars'] = Variable.objects.all().filter(catalog__id=case.id)
            child['operations'] = get_case_operations(case)
            module_suite['children'].append(child)
        result.append(module_suite)

    data = {
        'template': template,
        'project_vars': project_vars,
        'modules': modules,
    }
    print data

    return render(request, 'ui/project.html', {'project_id':pk})

def project_reports(request, pk):
    return render(request, 'ui/report.html',{'project_id':pk})