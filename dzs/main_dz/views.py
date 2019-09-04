from django.shortcuts import render
from django.views.generic import View
from api.models import *
from api.utils import *
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import quote
from django.utils.encoding import force_text
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.
def main_dz(request):
    return render(request, 'index.html', context= {})





class ListDebitors(ListView):
  model = Debitor
  paginate_by = 10
  template_name = 'main_dz/sp_debitors.html'

  def get_queryset(self):
    sr=force_text(self.request.GET.get('search', ''))
    if sr:
      return self.model.objects.filter(Q(title__icontains=sr)|Q(inn__icontains=sr))
    else:
      return self.model.objects.all()




class DebDetail(DetailView):
   template_name = 'main_dz/deb_detail.html'
   model = Debitor
   pk_url_kwargs = 'slug'
   context_object_name = 'deb'

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['debs'] = self.model.objects.filter(inn = context['object'].inn).exclude(slug= context['object'].slug)
        context['scheta'] = Schet.objects.filter(vlad= context['object'])
        return context
