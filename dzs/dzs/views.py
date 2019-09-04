from django.shortcuts import redirect
from django.http import HttpResponse

def redirect_m(request):
  return redirect('main_dz_url', permanent = True)


 