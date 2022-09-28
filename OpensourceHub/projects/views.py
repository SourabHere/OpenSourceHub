from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projectsObj=Project.objects.all()
    files={'Projects':projectsObj}
    return render(request,"projects/allprojs.html",files)


def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    tags=projectObj.tags.all()
    files={'Project':projectObj ,'tags':tags }
    return render(request,"projects/Selected.html",files)

@login_required(login_url="login")
def createProject(request):
    form=ProjectForm()

    if request.method=='POST':
        form=ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('projects')


    context={"form": form}
    return render(request,"projects/Addproj.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    project=Project.objects.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)

        if form.is_valid():
            form.save()
            return redirect('projects')


    context={"form": form}
    return render(request,"projects/Addproj.html",context)

@login_required(login_url="login")
def deleteProjects(request, pk):
    project=Project.objects.get(id=pk)
    context={'object':project}

    if request.method=='POST':
        project.delete()
        return redirect('projects')

    return render(request,"projects/deletetemp.html",context)