from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Catalog
from serializers import *
from libs.functions import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def catalog_list(request, scope):
    """
    List all code catalogs, or create a new catalog.
    """
    scope_list = ['projects', 'modules', 'templates', 'cases']
    if scope in scope_list:
        scope = scope[0:-1].capitalize()
        if request.method == 'GET':
            catalogs = Catalog.objects.all().filter(type=scope)
            serializer = CatalogSerializer(catalogs, many=True)
            return JSONResponse(serializer.data)

        elif request.method == 'POST':
            print str(request.body)
            data = JSONParser().parse(request)
            data["type"] = scope
            data["status"] = 0
            if scope == 'Project':
                data["parent_id"] = -1
            serializer = CatalogSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=200)
            return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def catalog_detail(request, scope, pk):
    """
    Retrieve, update or delete a code catalog.
    """
    scope_list = ['projects', 'modules', 'templates', 'cases']
    if scope in scope_list:
        scope = scope[0:-1].capitalize()
        try:
            catalog = Catalog.objects.all().get(pk=pk)
        except Catalog.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            print "get:"+str(catalog)
            serializer = CatalogSerializer(catalog)
            return JSONResponse(serializer.data)

        if request.method == 'PUT':
            print "put:"+str(catalog)
            data = JSONParser().parse(request)
            serializer = CatalogSerializer(catalog, data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=400)

        if request.method == 'DELETE':
            print "delete:"+str(catalog)
            catalog.delete()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def var_list(request, scope, scope_id):
    """
    List all code catalogs, or create a new catalog.
    """
    scope_list = ['projects', 'modules', 'templates', 'cases']
    if scope in scope_list:
        if request.method == 'GET':
            vars = Variable.objects.all().filter(catalog__id=scope_id)
            serializer = VariableSerializer(vars, many=True)
            return JSONResponse(serializer.data)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = CatalogSerializer(data=data)
            serializer.type = scope
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def var_detail(request, scope, scope_id, var_id):
    """
    Retrieve, update or delete a code catalog.
    """
    scope_list = ['projects', 'modules', 'templates', 'cases']
    if scope in scope_list:
        scope = scope[0:-1].capitalize()
        try:
            catalogs = Catalog.objects.all().filter(pk=scope_id,type=scope)
            if len(catalogs) > 0:
                catalog = catalogs[0]
            else:
                return HttpResponse(status=404)
        except Catalog.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = CatalogSerializer(catalog)
            return JSONResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = CatalogSerializer(catalog, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            catalog.delete()
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)


@csrf_exempt
def project_list(request):
    """
    List all code catalogs, or create a new catalog.
    """

    if request.method == 'GET':
        catalogs = Catalog.objects.all().filter(type='Project')
        serializer = CatalogSerializer(catalogs, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CatalogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def project_detail(request, pk):
    """
    Retrieve, update or delete a code catalog.
    """
    try:
        catalog = Catalog.objects.all().filter(pk=pk,type='Project')[0]
    except Catalog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CatalogSerializer(catalog)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CatalogSerializer(catalog, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        catalog.delete()
        return HttpResponse(status=204)


def test(request,pk):
    try:
        Catalog.objects.get(pk=pk)
    except Catalog.DoesNotExist:
        return HttpResponse(status=404)

    run(pk)

    return HttpResponse(status=200)

