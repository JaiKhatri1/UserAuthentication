from django.contrib import admin
from django.urls import path
from UserApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.user_signup,name='SignUp'),
    path('login/',views.user_login,name='LogIn'),
    path('profile/',views.user_profile,name='Profile'),
       path('logout/',views.user_logout,name='LogOut'),
       path('request_evaluation/', views.request_evaluation, name='request_evaluation')

]