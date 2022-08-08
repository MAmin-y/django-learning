import re
from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import search_project, paginate_project
from django.contrib import messages


def projects(request):
    projects, search_query = search_project(request)
    custom_range , projects= paginate_project(request, projects, 3)
    args = {
        "projects" : projects ,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'projects.html', args)


def single_project(request, argum):
    project = Project.objects.get(id = argum)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project =project
        review.owner = request.user.profile
        review.save()
        project.get_vote_count
        messages.success(request, 'Your Review was successfully submitted! ')
        return redirect('single_project', argum = project.id)

    args = {
        'project': project,
        'form': form
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

