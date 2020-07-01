"""trafficviolationbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path

from videoreport import views

urlpatterns = [
    path('', views.index, name="home"),
    path('videoreport/', views.get_report, name="videoreport"),
    path('download/', views.download, name="download"),
    #path('download_file/', views.download_file, name="download_file"),
    #path('/static/Violated_cars/violated_data.csv', views.download_file, name='download_file'),
    path('admin/', admin.site.urls),
]

