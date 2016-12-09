from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'ui/index.html')


def project_detail(request, pk):
    return render(request, 'ui/project.html', {"project_id":pk})