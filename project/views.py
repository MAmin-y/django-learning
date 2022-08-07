from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from .utils import search_project
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def projects(request):
    projects, search_query = search_project(request)

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except EmptyPage:                                       # age ye page bishtar az mojood dade shod boro page akhar
        page = paginator.num_pages
        projects = paginator.page(page)
    except PageNotAnInteger:                                # defult page 1 bashe
        page = 1
        projects = paginator.page(page)

    args = {
        "projects" : projects ,
        'search_query': search_query,
        'paginator': paginator
    }
    return render(request, 'projects.html', args)


def single_project(request, argum):
    
    args = {
        'project': Project.objects.get(id = argum)
    }
    return render(request, 'single_project.html', args)


@login_required(login_url= "login")
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit= False)    # ye mesal azash bede vali save nakon
            project.owner = request.user.profile
            project.save()
            return redirect('user_account')

    args = {
        'form': form
    }
    return render(request, 'project_form.html', args)


@login_required(login_url= "login")
def update_project(request, argum):
    profile = request.user.profile
    proj = profile.project_set.get(id = argum)   
    # proj = Project.objects.get(id = argum)      # intori age ye karbar dige id project ro bedoone taghiiresh mide pas khat bala jaygozin shod
    form = ProjectForm(instance= proj)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=proj)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    args = {
        'form': form
    }
    return render(request, 'project_form.html', args)


@login_required(login_url= "login")
def delete_project(request, argum):
    profile = request.user.profile
    proj = profile.project_set.get(id = argum) 
    if request.method == 'POST':
        proj.delete()
        return redirect("home")
    args = {
        'object': proj
    }
    return render(request, 'delete_template.html', args)

