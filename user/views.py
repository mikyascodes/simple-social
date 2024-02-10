from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from user.models import UserProfile
from .forms import RegistrationForm, ProfileForm, UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def login_view(request) :  
    complete_profile_url = reverse('complete_profile')
    profile_url = reverse('profile')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Get the user's profile object.
            profile = UserProfile.objects.get(user=user)
            # Check if the profile is complete.
            if not profile.profile_status or not profile.avatar:
                login(request, user)
                messages.error(request, 'Please complete your profile and upload a file before logging in')
                return redirect(complete_profile_url)
            else:
                # The profile is complete, so log in the user and redirect them to the profile page.
                login(request, user)
                return redirect(profile_url)
    else:
        form = AuthenticationForm(data=request.POST)
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'registration/home.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html',{'form': form})
   

@login_required
def profile(request):
    users = UserProfile.objects.exclude(user=request.user)
    return render(request, 'usingsite/profile.html',{'users': users})
    

def home(request):
    return render(request, 'registration/home.html')

@login_required
def complete_profile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    if request.method == 'POST':
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'registration/profile_incomplete.html', {'form': form, 'u_form':u_form})
    return render(request, 'registration/profile_incomplete.html', {'form': form, 'u_form':u_form})


@login_required
def view_profile(request, pk):
    try:
        user = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        # Handle the case where the UserProfile object does not exist
        return HttpResponseNotFound('User profile not found')
    context = {
        'user': user,
    }
    return render(request, 'usingsite/view_profile.html', context)


@login_required
def friends_view(request):
    following = request.user.userprofile.following.all()
    return render(request, 'usingsite/friends.html', {'following': following})


@login_required
def add_user(request,pk):
    if request.method=='POST':
        users = UserProfile.objects.get(pk=pk)
        current_user = request.user
        data = request.POST['follow']
        if data == 'follow':
            current_user.userprofile.following.add(users)
            current_user.userprofile.save()
            messages.add_message(request, messages.SUCCESS,  f'you and {users.user.username} are now friends')
            return render(request,'usingsite/friends_now.html' ,{'users':users})
        elif data == 'unfollow':
            current_user.userprofile.following.remove(users)
            current_user.userprofile.save()
            messages.add_message(request, messages.SUCCESS, f'You have unfollowed {users.user.username}') 
            return redirect(reverse('profile'))
    return redirect(reverse('profile'))

