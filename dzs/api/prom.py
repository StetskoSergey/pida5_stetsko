class Debitor(models.Model):
  VID_UR = (('ОАО', 'ОАО'), ('ООО', 'ООО'), ('ЗАО', 'ЗАО'), ('ИП', 'ИП'),('НР', 'Нерезидент'),)
  type = models.BooleanField()
  p_title = models.CharField(max_length= 150, db_index = True)
  title = models.CharField(max_length= 150, db_index = True)
  ur_forma = models.CharField(max_length= 3, db_index = True, blank = True, choices = VID_UR)
  inn = models.CharField(max_length=12, db_index=True, blank = True)
  kpp = models.CharField(max_length=10, db_index=True, blank = True)
  slug = models.SlugField(max_length=50,db_index=True, unique=True )

  def __str__(self):
    return self.title
  
  def gen_slug(self):
     if not self.slug: 
       if self.inn:
         self.slug  = self.inn
       else:
         self.slug=slugify(self.title[:50], allow_unicode=True)
 
  def save(self, *args, **kwargs):
    self.gen_slug()
    super().save(*args, **kwargs)
    
    
    def proverka():
  for i in Debitor.objects.all():
    i.save()
    
    
 Create your views here.
def sp_debitors(request):
  return render(request, 'sp_debitors.html', context={'debs':Debitor.objects.all()})
