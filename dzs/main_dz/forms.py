from django import forms
from api.models import *
from django.core.exceptions import ValidationError

class DebitorForm(forms.ModelForm):

  
  class Meta:
    model = Debitor
    
    widgets = {
      'title': forms.TextInput(attrs= {"class":"form-conttol"}),
      'slug': forms.TextInput(attrs= {"class":"form-conttol"})
    
    }
  
  
    
    
class DolgForm(forms.ModelForm):

  
  class Meta:
    model = Dolg
    
    
    widgets = {
      'title': forms.TextInput(attrs= {"class":"form-conttol"}),
      'slug': forms.TextInput(attrs= {"class":"form-conttol"}),
      'body': forms.Textarea(attrs= {"class":"form-conttol"}),
      'tags': forms.SelectMultiple(attrs= {"class":"form-conttol"})
    
    }
  
  
    
  