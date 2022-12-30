"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from MyApp import views as App_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('MyApp/',include('MyApp.urls')),
    path('login/',App_views.login),
    path('student_register/',App_views.student_register),
    path('manager_register/',App_views.manager_register),
    path('login_judge/', App_views.login_judge),
    path('student_information/',App_views.student_information),
    path('search_book/',App_views.search_book),
    path('borrow_record/',App_views.borrow_record),
    path('change_password/',App_views.change_password),
    path('borrow_book/',App_views.borrow_book),
    path('return_book/',App_views.return_book),
    path('manager_information/', App_views.manager_information),
    path('manage_book/', App_views.manage_book),
    path('delete_book/', App_views.delete_book),
    path('add_book/', App_views.add_book),
    path('reduce_book/', App_views.reduce_book),
    path('change_manager_password/', App_views.change_manager_password),
    path('add_new_book/', App_views.add_new_book),
    path('alter_book/', App_views.alter_book),
    path('',App_views.login),
]