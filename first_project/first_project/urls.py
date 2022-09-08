"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from middleapp import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('' , views.index , name= "home"),
  path('delete/' , views.delete_all , name= "delete"),
  path('application_cms/', views.cms_post),
  path('application_get_cms/', views.cms_get),
  path('md/<str:st>', views.enc_post),
]
