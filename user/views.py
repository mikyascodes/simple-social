from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from user.models import Message, Notification, UserProfile
from django.contrib.auth.models import User
from .forms import RegistrationForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def login_view(request):
    complete_profile_url = reverse("complete_profile")
    profile_url = reverse("profile")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Get the user's profile object.
            profile = UserProfile.objects.get(user=user)
            # Check if the profile is complete.
            if not profile.profile_status or not profile.avatar:
                login(request, user)
                messages.add_message(
                    request,
                    messages.INFO,
                    "Please complete your profile and upload a file before logging in",
                )
                return redirect(complete_profile_url)
            else:
                # The profile is complete, so log in the user and redirect them to the profile page.
                login(request, user)
                return redirect(profile_url)
    else:
        form = AuthenticationForm(data=request.POST)
    return render(request, "registration/login.html", {"form": form})


def signup(request):
    form = RegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return render(request, "registration/home.html")
    else:
        form = RegistrationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    users = UserProfile.objects.exclude(user=request.user)
    return render(request, "usingsite/profile.html", {"users": users})


def home(request):
    return render(request, "registration/home.html")


@login_required
def complete_profile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    if request.method == "POST":
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        form = ProfileForm(instance=request.user.userprofile)
        return render(
            request,
            "registration/profile_incomplete.html",
            {"form": form, "u_form": u_form},
        )
    return render(
        request,
        "registration/profile_incomplete.html",
        {"form": form, "u_form": u_form},
    )


@login_required
def view_profile(request, pk):
    user = UserProfile.objects.get(pk=pk)
    recipient = User.objects.get(pk=pk)
    if request.method == "POST":
        content = request.POST.get("content")
        sender = request.user
        message = Message.objects.create(
            sender=sender, recipient=recipient, content=content
        )
        Notification.objects.create(user=recipient, message=message)
        return redirect("view_profile", pk=pk)
    messages = Message.objects.filter(
        sender=request.user, recipient=recipient
    ).order_by("timestamp") | Message.objects.filter(
        sender=recipient, recipient=request.user
    ).order_by(
        "timestamp"
    )
    return render(
        request,
        "usingsite/view_profile.html",
        {"user": user, "recipient": recipient, "messages": messages},
    )


@login_required
def friends_view(request):
    following = request.user.userprofile.following.all()
    return render(request, "usingsite/friends.html", {"following": following})


@login_required
def add_user(request, pk):
    if request.method == "POST":
        users = UserProfile.objects.get(pk=pk)
        current_user = request.user
        data = request.POST["follow"]
        if data == "follow":
            current_user.userprofile.following.add(users)
            current_user.userprofile.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"you and {users.user.username} are now friends",
            )
            return render(request, "usingsite/friends_now.html", {"users": users})
        elif data == "unfollow":
            current_user.userprofile.following.remove(users)
            current_user.userprofile.save()
            messages.add_message(
                request, messages.SUCCESS, f"You have unfollowed {users.user.username}"
            )
            return redirect(reverse("profile"))
    return redirect(reverse("profile"))


def check_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, read=False)
        data = [
            {
                "message": notification.message.content,
                "created_at": notification.created_at,
                "sender": notification.message.sender.username,
                "sender_avatar_url": notification.message.sender.userprofile.avatar.url,
            }
            for notification in notifications
        ]
        return JsonResponse({"notifications": data})
    else:
        return JsonResponse({"notifications": []})


@login_required
def notifications(request):
    return render(request, "usingsite/notification.html")


@require_POST
def update_notification_status(request):
    if request.user.is_authenticated:
        notification_id = request.POST.get("notification_id")
        try:
            notification = Notification.objects.get(
                id=notification_id, user=request.user
            )
            notification.read = True
            notification.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notification not found"})
    else:
        return JsonResponse({"success": False, "error": "User is not authenticated"})
