"""
URL configuration for task04 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import task1.views as subview01
import task2.views as subview02
import task3.views as subview03
import task4.views as subview04

urlpatterns = [
    path('sub01', subview01.to_sub01),
    path('sub02', subview02.to_sub02),
    path('sub03', subview03.to_sub03),
    path('sub04', subview04.to_sub04),
    path('sub01/getData', subview01.get_data),
    path('sub02/getData', subview02.get_data),
    path('sub02/setData', subview02.set_data),
    path('sub03/getData', subview03.get_data),
    path('sub03/setData', subview03.set_data),
    path('sub04/getLineData', subview04.get_line_data),
    path('sub04/getBarData', subview04.get_bar_data),
]
