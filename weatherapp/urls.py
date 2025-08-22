from django.contrib import admin
from django.urls import path
from weatherapp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name='home'),
    path('login', views.loginuser, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logoutuser, name='logout'),
    path('forgotpassword',auth_views.PasswordResetView.as_view( template_name='forgotpassword.html'),name='password_reset'),
    path('resetdone',auth_views.PasswordResetDoneView.as_view( template_name='resetdone.html'),name='password_reset_done'),
    path('resetconfirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view( template_name='resetconfirm.html'),name='password_reset_confirm'),
    path('resetcomplete',auth_views.PasswordResetCompleteView.as_view( template_name='resetcomplete.html'),name='password_reset_complete')
]