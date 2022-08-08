from re import A
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, paginate_profiles




def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range , profiles = paginate_profiles(request, profiles, 3)
    args = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request ,'users/profiles.html', args)


def user_profile(request, argum):
    profile = Profile.objects.get(id = argum)
    args = {
        'profile': profile,
        'topskills': profile.skill_set.exclude(description__exact=""), # oonaiike description nadarano hazfnmikone
        'otherkills': profile.skill_set.filter(description="")  # oonaiike description nadarano mide
    }
    return render(request, 'users/profile.html', args)

def loginuser(request):

    # if request.user.is_authenticated:
    #     return redirect('projects')

    # t
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User not found")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if "next" in request.GET else 'user_account')
        else:
            messages.error(request,"username or password is incorrect")

    args = {
        'page_type' : 'login'
    }

    return render(request, 'users/login_user.html', args)



def logoutuser(request):
    logout(request)
    messages.info(request,"user was successfully logged out")
    return redirect('login')

def register_user(request):
    form = CustomUserCreationForm()
    

    if request.method == 'POST': 
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"user was successfully registered")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request,"an error occurred while registering")
            
    args = {
        'page_type' : 'register',
        'form' : form
    }
    return render(request, 'users/login_user.html', args)


@login_required(login_url= "login")
def user_account(request):
    profile = request.user.profile
    args ={
        'profile': profile,
        'skills': profile.skill_set.all(),
        'projects': profile.project_set.all()
    }
    return render(request, 'users/user_account.html', args)


@login_required(login_url= "login")
def edit_account(request):
    profile  = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('user_account')
    
    args ={
        'form': form
    }
    return render(request, 'users/profile_form.html', args)


@login_required(login_url= "login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill Was Added successfully")
            return redirect('user_account')
    args = {
        'form': form
    }
    return render(request, 'users/skill_form.html', args)


@login_required(login_url= "login")
def update_skill(request, argum):
    profile = request.user.profile
    skill = profile.skill_set.get(id = argum)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill Was Updated successfully")
            return redirect('user_account')
    
    args = {
        'form': form
    }
    return render(request, 'users/skill_form.html', args)

def delete_skill(request, argum):
    profile = request.user.profile
    skill = profile.skill_set.get(id = argum)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,"Skill Was Deleteed successfully")
        return redirect('user_account')
    args = {
        'object': skill
    }
    return render (request, 'delete_template.html')