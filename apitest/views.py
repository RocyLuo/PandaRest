from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Catalog
from serializers import CatalogSerializer
from libs.Runner import Runner


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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

@csrf_exempt
def project_module_list(request, pk):
    """
    List all code catalogs, or create a new catalog.
    """

    if request.method == 'GET':
        modules = Catalog.objects.all().filter(parent__id=pk,type='Module')
        serializer = CatalogSerializer(modules, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def module_post(request):
    """
    List all code catalogs, or create a new catalog.
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CatalogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def module_detail(request, module_pk):
    """
    Retrieve, update or delete a code catalog.
    """
    try:
        catalog = Catalog.objects.all().filter(pk=module_pk,type='Module')[0]
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

@csrf_exempt
def module_case_list(request, pk):
    """
    List all code catalogs, or create a new catalog.
    """
    if request.method == 'GET':
        modules = Catalog.objects.all().filter(parent__id=pk,type='Case')
        serializer = CatalogSerializer(modules, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def case_post(request):
    """
    List all code catalogs, or create a new catalog.
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CatalogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def case_detail(request, case_pk):
    """
    Retrieve, update or delete a code catalog.
    """
    try:
        catalog = Catalog.objects.all().filter(id=case_pk,type='Case')[0]
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
        catalog = Catalog.objects.get(pk=pk)
    except Catalog.DoesNotExist:
        return HttpResponse(status=404)
    runner = Runner()
    runner.run(pk)

    return HttpResponse(status=200)

