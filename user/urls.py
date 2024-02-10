from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import add_user, signup, profile,home,complete_profile,login_view,view_profile, friends_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('home/',home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/home.html'),name='logout'),
    path('signup/', signup, name='signup'),
    path('friends_now/<int:pk>/', add_user, name='friends_now'),
    path('profile/', profile, name='profile'),
    path('complete_profile/', complete_profile, name='complete_profile'),  
    path('profile/<int:pk>/', view_profile, name='view_profile'),
    path('friends/', friends_view, name='friends'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name= "password_reset/password_reset_form.html"), name='password_reset'), 
    path('reset-password/done', auth_views.PasswordResetDoneView.as_view(template_name= "password_reset/password_reset_done.html"), name='password_reset_done'), 
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= "password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset-password/complete/',auth_views.PasswordResetCompleteView.as_view(template_name= "password_reset/password_reset_complete.html"),name='password_reset_complete'),
]
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
