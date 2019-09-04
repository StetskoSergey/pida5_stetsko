from django.shortcuts import render
from django.views.generic import View
from .models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import Http404
from .utils import *
from django.http import JsonResponse



# Create your views here.
def test(request):
  print(dir(request))
  print(request.headers)
  print(request.COOKIES)

  rt=Tek(request)
  sl = {'m':'login',
           'id': 'rhs' ,
           'u' : 'test' ,
           'l'  : 'testtest314'
  }
  rt.identification(sl)
  return rt.resp

def subscribers_existence(request):
     rt=Tek(request)
     if rt.resp:
         return rt.resp
     return JsonResponse({'status': 'ok'})

def debitor_existence(request):
     rt=Tek(request)
     if rt.resp:
         return rt.resp
     rt.debitor_existence()
     if rt.resp:
         return rt.resp
     return JsonResponse({'status': 'ok'})

def debitor_create(request):
     rt=Tek(request)
     if rt.resp:
         return rt.resp
     print (rt.sl)
     for dannie in rt.sl:
         res, debitor = rt.zapisDebitor(dannie)
         if not res:
             return rt.resp
         res, shet = rt.zapisSheta(dannie,debitor)
         if not res:
             return rt.resp
     return JsonResponse({'status': 'ok'})

def history_create(request):
     #print('headers',request.headers)
     #print('post',request.POST)
     #print('get',request.GET)
     rt=Tek(request)
     if rt.resp:
         return rt.resp
     rt.zapisDvj()
     if rt.resp:
         return rt.resp
     return JsonResponse({'status': 'ok'})

def dolg_create(request):
     #print('headers',request.headers)
     #print('post',request.POST)
     #print('get',request.GET)
     rt=Tek(request)
     if rt.resp:
         return rt.resp
     rt.zapisDolg()
     if rt.resp:
         return rt.resp
     return JsonResponse({'status': 'ok'})


def api(request):
  rt=Tek(request)
  # print('body', type(rt.sl))
  # print('body', rt.sl)
  rt.identification()
  if not rt.login:
    return rt.resp
  if rt.post:
    rt.obrabotka()
  return rt.resp
