from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.core import paginator 

# Create your views here.

def paginateProjects(request, projects, results):

    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects

def projects(request):
    search_query=''

    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')

    tags=Tag.objects.filter(name__icontains=search_query)
    projectsObj=Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query)|
        Q(tags__in=tags)
    )

    
    
    custom_range,projectsObj =paginateProjects(request,projectsObj,6)




    files={'Projects':projectsObj,'search_query':search_query, 'custom_range':custom_range}
    return render(request,"projects/allprojs.html",files)


def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    tags=projectObj.tags.all()
    form=ReviewForm()

    if request.method=="POST":
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.Project=projectObj
        review.owner=request.user.profile
        review.save()

        projectObj.getVoteCount
        messages.success(request,"Successfully uploaded your review.")
        return redirect('project',pk=projectObj.id)

    files={'Project':projectObj ,'tags':tags, 'form':form }
    return render(request,"projects/Selected.html",files)

@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form=ProjectForm()

    if request.method=='POST':
        form=ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            return redirect('projects')


    context={"form": form}
    return render(request,"projects/Addproj.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
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
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    context={'object':project}

    if request.method=='POST':
        project.delete()
        return redirect('projects')

    return render(request,"delete.html",context)