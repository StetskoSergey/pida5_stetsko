from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User
# Create your models here.

def gen_slug(s):
  return slugify(s, allow_unicode=True)+"-"+str(int(time()))

class Company(models.Model):

  slug = models.SlugField(max_length=50,db_index=True,unique=True)
  title = models.CharField(max_length= 150, db_index = True, unique = True)
  date_pub = models.DateTimeField(auto_now_add = True)
  key = models.SlugField(max_length=100,db_index=True,unique=True, null = True)

  class Meta:
    ordering = ['-date_pub']

  def save(self, *args, **kwargs):
    if not self.id and not self.slug:
      self.slug = gen_slug(self.title[:50])
    super().save(*args, **kwargs)

  def __str__(self):
    return self.title

class CompanyUsers(models.Model):

  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  user_n = models.ForeignKey(User, on_delete=models.CASCADE)
  key = models.SlugField(max_length=100,db_index=True, unique=True, null = True)
  key_refresh = models.SlugField(max_length=100,db_index=True,unique=True, null = True)
  key_d = models.DateField(null = True)


  def __str__(self):
    return self.user_n.username

class UrForma(models.Model):
  VID_UR = (('ОАО', 'ОАО'), ('ООО', 'ООО'), ('ЗАО', 'ЗАО'), ('Индивидуальный предприниматель','ИП'),( 'Нерезидент','НР'),('',''),)
  title = models.CharField(max_length=60, db_index = True, blank = True, choices = VID_UR)
  short = models.CharField(max_length=3, db_index = True, blank = True)

  def __str__(self):
    return self.title

class UrType(models.Model):
  TIP_UR = (('Юридическое лицо', 'ЮрЛицо'), ('Физическое лицо','ФизЛиц'), ('Индивидуальный предприниматель','ИП'),('Нерезидент','НР'),('',''),)
  title = models.CharField(max_length=60, db_index = True, blank = True, choices = TIP_UR)
  short = models.CharField(max_length=10, db_index = True, blank = True)

  def __str__(self):
    return self.title

class Bank(models.Model):
  title = models.CharField(max_length=150, db_index = True)
  bic = models.CharField(max_length=10, db_index = True, unique = True)


class Debitor(models.Model):
  ur_type = models.ForeignKey(UrType, on_delete=models.CASCADE)
  p_title = models.CharField(max_length= 150, db_index = True)
  title = models.CharField(max_length= 150, db_index = True)
  ur_forma = models.ForeignKey(UrForma, on_delete=models.CASCADE)
  inn = models.CharField(max_length=12, db_index=True, unique= True)
  kpp = models.CharField(max_length=10, db_index=True)
  u_adress = models.CharField(max_length= 150, db_index = True)
  f_adress = models.CharField(max_length= 150, db_index = True, blank = True)
  telef = models.CharField(max_length= 100, db_index = True, blank = True)
  slug = models.SlugField(max_length=50,db_index=True,unique=True)

  def __str__(self):
    return self.title

  def get_absolut_url(self):
    return reverse('deb_detail_url', kwargs={'slug':self.slug})

  class Meta:
    ordering = ['title']

class Schet(models.Model):
  n_scheta = models.CharField(max_length=40, db_index = True)
  bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
  vlad = models.ForeignKey(Debitor, on_delete=models.CASCADE, null = True)

class Valuta(models.Model):
  title = models.CharField(max_length= 50)
  s_title = models.CharField(max_length= 3)
  kod = models.CharField(max_length= 3, unique = True)

  def __str__(self):
    return self.title

class Dogovor(models.Model):
  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  kreditor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='Dogovor_kreditor')
  debitor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='Dogovor_debitor')
  title = models.CharField(max_length= 150, db_index = True, blank = True)
  date = models.DateField(blank = True)
  date_end = models.DateField(blank = True)
  valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
  uiid = models.CharField(max_length= 40, db_index = True)

  def __str__(self):
    return str([self.title, self.kreditor.title, self.debitor.title])


class ObRash(models.Model):
  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  kreditor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='ObRash_kreditor')
  debitor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='ObRash_debitor')
  title = models.CharField(max_length= 150, db_index = True, blank = True)
  uiid = models.CharField(max_length= 40, db_index = True)

  def __str__(self):
    return str([self.title, self.kreditor.title, self.debitor.title])


class OutputId(models.Model):
  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  uiid = models.CharField(max_length= 40)
  debitor = models.ForeignKey(Debitor,on_delete=models.CASCADE, null = True)
  dogovor = models.ForeignKey(Dogovor,on_delete=models.CASCADE, null = True)
  ob_rash = models.ForeignKey(ObRash,on_delete=models.CASCADE, null = True)

  def __str__(self):
    return self.uiid

class Dolg(models.Model):
  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  kreditor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='kreditor')
  debitor = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='debitor')
  ob_rash = models.ForeignKey(ObRash, on_delete=models.CASCADE, related_name='ob_rash')
  date_r= models.DateField()
  pogashen = models.BooleanField()
  perv_summa = models.FloatField()
  ost_summa= models.FloatField()
  valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
  date_pogashenia = models.DateField()
  prosr = models.IntegerField()
  dogovor = models.ForeignKey(Dogovor, on_delete=models.CASCADE, related_name='dogovor')
  uiid_dolg = models.CharField(max_length= 40, db_index = True)

  def __str__(self):
    return str([self.id_company, self.kreditor, self.debitor, self.perv_summa,self.date_r ])


class History(models.Model):
  id_company =models.ForeignKey(Company, on_delete=models.CASCADE)
  ob_rash = models.ForeignKey(ObRash, on_delete=models.CASCADE)
  date_d = models.DateField()
  summ = models.FloatField()
  valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
  document = models.CharField(max_length= 150, db_index = True, blank = True)
  uiid_document = models.CharField(max_length= 40, blank = True)

  def __str__(self):
    return str([self.ob_rash, self.date_d, self.summ, self.document])


class Acc(models.Model):
  vlad = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='vlad')
  doch = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='doch')
  share = models.IntegerField()

  def __str__(self):
    return str([self.vlad.title, self.doch.title, self.share])

class SvLitsa(models.Model):
  vid_svyzi = models.CharField(max_length= 50, db_index = True)
  osn = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='osn')
  sv = models.ForeignKey(Debitor, on_delete=models.CASCADE, related_name='sv')

  def __str__(self):
    return str([self.osn.title, self.sv.title, self.vid_svyzi])
