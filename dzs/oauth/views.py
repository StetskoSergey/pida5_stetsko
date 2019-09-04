from django.shortcuts import render
from api.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import Http404
from api.utils import *
from django.http import JsonResponse

# Create your views here.
def get_key(request):
    #print(dir(request))
    print('headers',request.headers)
    print('post',request.POST)
    print('get',request.GET)

    rt=Tek(request)
    if rt.resp:
        return rt.resp
    rt.get_token()
    return rt.resp
