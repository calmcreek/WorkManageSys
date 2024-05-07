from django.shortcuts import render
from .models import Role, Work, Worker, WorkRoleRequirement
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def employeelist(request):
    emps = Worker.objects.all()
    context = {
        'emps' : emps 
    }
    return render(request, 'employeelist.html', context)

def ourwork(request):
    works = Work.objects.all()
    context = {
        'works': works
    }
    return render(request, 'ourwork.html', context)

def worker_detail(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    assigned_works = worker.assigned_works.all()
    return render(request, 'worker_detail.html', {'worker': worker, 'assigned_works': assigned_works})