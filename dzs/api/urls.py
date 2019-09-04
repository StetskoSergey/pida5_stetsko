"""blogengine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from .views import *


urlpatterns = [
    path('', api, name = "api_url"),
    path('test/',test),
    path('core/v1/subscribers/existence', subscribers_existence, name = "api_subscribers_existence_url"),
    path('core/v1/debitor/existence', debitor_existence, name = "api_debitor_existence_url"),
    path('core/v1/debitor/create', debitor_create, name = "api_debitor_create_url"),
    path('core/v1/dolg/create', dolg_create, name = "api_dolg_create_url"),
    path('core/v1/history/create', history_create, name = "api_history_create_url"),

]
