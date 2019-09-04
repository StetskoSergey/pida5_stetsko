from django.shortcuts import render
from django.views.generic import View
from django.utils.text import slugify
from .models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.serializers.json import json
from secrets import token_urlsafe
from datetime import timedelta,date


# Create your views here.
class Tek:
  company=None
  user = None
  login = False
  request = None
  sl = []
  sid = []
  resp = None
  post = False
  valuta = None

  def AuthToken(self, au):
    # ищет ключ в базе ключей по идентификатору,
    # по ключу делает идентификацию
    # нужно декодировать ключ вначале ...
    if not au:
        return ''
    if au[0]=='Basic':
        key = urlsafe_base64_decode(au[1])
        key = key[:len(key)-1].decode()
        q = Company.objects.filter(key = key)
        if q:
            self.company = q[0]
            return True
        else:
            return False
    elif au[0]=='Bearer':
        key = au[1]
        q = CompanyUsers.objects.filter(key = key)
        if q:
            self.company = q[0].id_company
            self.user = q[0].user_n
            return True
        else:
            return False






  def __init__(self, request):
    self.request= request
    au = request.headers.get('Authorization','')
    if au:
        au = au.split(' ')
        if not self.AuthToken(au):
            self.err_d('Token ne nayden')
    if self.request.method == 'GET':
      self.sid = self.request.GET
    elif self.request.method == 'POST':
      self.sid = self.request.GET
      if self.request.body:
          self.sl = json.loads(self.request.body)
      self.post = True
    else:
      self.err_d('Metod ne opredelen')

  def otvet(  self, res):
    return JsonResponse({'status': res})

  def err_d(  self, res):
    # error_description
    self.resp = JsonResponse({'error_description': res})
    self.resp.status_code = 500


  def GenerateToken(self, userC, polnoe_obnovlenie):
    if not polnoe_obnovlenie:
      if userC.key_d < date.today():
        self.err_d('srok token istek')
        return False
    else :
      userC.key = token_urlsafe(60)
      userC.key_refresh  = token_urlsafe(60)
      userC.key_d = date.today()+ timedelta(days= 10)
      userC.save()
    self.resp = JsonResponse({'access_token': userC.key,
             'refresh_token' : userC.key_refresh,
             'expires_in' : (userC.key_d - date.today()).days*3600*24
              })
    return True



  def __str__(self):
     return str(self.sl)

  def get_token(self):
    if not self.company:
         return False
    m_get = self.sid.get('grant_type', '')
    if not m_get:
        return False
    if m_get == 'password':
        u = self.sid['username']
        l = self.sid['password']
        self.user = authenticate(self.request, username=u, password=l)
        if self.user is not None:
            q = CompanyUsers.objects.filter(id_company=self.company, user_n = self.user)
            if not q :
              self.err_d('Polzovatel companiy ne nayden')
              return False
            else:
              userC = q[0]
              # генерим ключи ...
              return self.GenerateToken(userC, True)


        else:
            self.err_d(' Polzovatel ne nayden ')
            return False
    elif m_get == 'refresh_token':
          #  находим пользователя по ключу
          key = self.sid['refresh_token']
          q = userCompany.objects.filter( key_refresh = key, id_company = self.company)
          if q:
            userC = q[0]
            return self.GenerateToken(userC, False)

          else :
            self.err_d('Token ne nayden')
            return False


  def identification(self, sid=[]):
    if self.login:
      return True
    if not self.company:
        return False
    if sid:
      self.sid = sid
    m_get = self.sid.get('grant_type', '')
    if m_get == 'password':
        u = self.sid['username']
        l = self.sid['password']
        self.user = authenticate(self.request, username=u, password=l)

        if self.user is not None:
            q = CompanyUsers.objects.filter(id_company=self.company, user_n = self.user)
            if not q :
              self.resp = self.otvet('Polzovatel companiy ne nayden')
              return False
            else:
              userCompany = q[0]
              login(self.request, self.user)
              self.login = True
        else:
            self.resp= self.otvet(' Polzovatel ne nayden ')
            return False
    elif m_get == 'key':
      # авторизация по ключу
      key = self.sid.get('key', '')
      q=Company.objects.filter(key=key)
      if not q:
          self.resp = self.otvet('Compania ne naydena')
          return False
      else:
          self.company = q[0]
          q= CompanyUsers.objects.filter(id_company=self.company)
          if q:
            self.user = authenticate(self.request, username=q[0].user_n.username,  password= q[0].user_n.password)
            if self.user is not None:
              login(self.request, self.user)
              self.login = True
            else:
              self.resp= self.otvet(' Polzovatel ne nayden ')
              return False
          else:
            self.resp = self.otvet('Polzovatel companiy ne nayden')
            return False
    else:
      self.resp= self.otvet('Metod GET ne opredelen')
      return False
    self.resp = self.otvet('ok')
    return True





  def zapisDolg(self):
    kreditor = self.findUIID('uiid_k', 'debitor')
    if kreditor is None:
      self.resp = self.otvet('kreditor')
      return False
    debitor = self.findUIID('uiid_d','debitor')
    if debitor is None:
      self.resp = self.otvet('debitor')
      return False
    if not self.findValuta():
      return False
    ob_rash= self.findUIID('ob_rash', 'ob_rash')
    if ob_rash is None:
        self.resp = self.otvet('ob_rash')
        return False
    dogovor = self.findUIID('uiid_dogovor','dogovor')
    if dogovor is None:
      self.resp = self.otvet('dogovor')
      return False
    dolg = Dolg(id_company= self.company, kreditor= kreditor, debitor= debitor, ob_rash= ob_rash , date_r= self.sl['date_r'], valuta = self.valuta, date_pogashenia = self.sl['date_pogashenia'], dogovor = dogovor , uiid_dolg= self.sl['uiid_dolg']  )
    try:
      dolg.full_clean()
    except ValidationError as e:
      self.resp = self.otvet('error dolg')
      return False
    dolg.save()
    self.resp = self.otvet('ok')
    return True



  def findUIID(self, rek, ff):
    uiid = self.sl['rek']
    usl = ff+'__isnull'
    q= OutputId.objects.filter(id_company= self.company, uiid= uiid, usl=False)
    if len(q)==1:
      return q[0][ff]
    else:
      return None

  def zapisBanka(self, dannie):
      sl = dannie
      bic = sl['bic']
      title = sl['bank']
      try:
          bank, is_create = Bank.objects.update_or_create(title= title, bic= bic)
      except ValidationError as e:
        self.err_d('error bank'+' '+e.messages)
        return False, None
      return True, bank

  def zapisSheta(self, dannie, debitor):
      sl = dannie
      res, bank = self.zapisBanka(dannie)
      if not res:
          return False
      n_scheta = sl['schet']
      try:
          shet, is_create = Schet.objects.update_or_create(n_scheta= n_scheta, vlad= debitor, bank = bank)
      except ValidationError as e:
        self.err_d('error bank'+' '+e.messages)
        return False, None
      return True, shet




  def zapisDebitor(self, dannie):
    # должна возвращать найденного Дебитора или сообщать что его нет
    sl = dannie
    inn = sl['inn']
    uiid = sl['uiid']
    kpp = sl['kpp']
    if inn and not inn.isdigit():
      self.err_d('error debitor'+' ne verniy inn')
      return False, None
    if kpp and not kpp.isdigit():
      self.err_d('error debitor'+' ne verniy kpp')
      return False, None
    ur_type = UrType.objects.get(short= sl['ur'])
    ur_forma =UrForma.objects.get(short= sl['u_forma'])
    title = sl['title']
    p_title = sl['p_title']
    u_adress = sl['u_adress']
    f_adress = sl['f_adress']
    telef = sl['telef']
    slug = ''
    if inn:
      slug  = inn
    if kpp:
      slug = slug +'-'+kpp
    if not slug:
      slug=slugify(title[:50], allow_unicode=True)
    if uiid:
        q = OutputId.objects.filter(id_company= self.company, uiid= uiid)
        if q:
            d = q[0].debitor
            d.inn = inn
            d.kpp = kpp
            d.ur_type = ur_type
            d.slug = slug
            d.ur_forma = ur_forma
            d.title = title
            d.p_title = p_title
            d.u_adress = u_adress
            d.f_adress = f_adress
            d.telef = telef
            try:
                d.save()
            except ValidationError as e:
              self.err_d('error debitor'+' '+e.messages)
              return False, None
            self.resp = self.otvet('ok')
            return True, d
    try:
        d, is_create = Debitor.objects.update_or_create(ur_type=ur_type, title=title, p_title=p_title, ur_forma = ur_forma, inn= inn, kpp= kpp, slug = slug, telef = telef, u_adress = u_adress, f_adress = f_adress)
        try:
            out, is_create = OutputId.objects.update_or_create(id_company= self.company, uiid= uiid, debitor= d)
        except ValidationError as e:
          self.err_d('error out'+' '+e.messages)
          return False, None
    except ValidationError as e:
      self.err_d('error debitor'+' '+e.messages)
      return False, None
    self.resp = self.otvet('ok')
    return True, d


  def findValuta(self):
    q = Valuta.objects.filter(kod=self.sl['kod'])
    if q:
      self.valuta = q[0]
      return True
    else:
      self.resp= self.otvet('Valuta ne naidena' +self.sl['kod'] )
      return False


  def zapisDvj(self):
    # нужно сначала удалить все предыдущие движения документа
    History.objects.filter(  id_company= self.company, uiid_document= self.sl['uiid_document']).delete()
    ob_rash= self.findUIID('ob_rash', 'ob_rash')
    if ob_rash is None:
        self.resp = self.otvet('ob_rash')
        return False
    if not self.findValuta():
      return False
    h = History(id_company=self.company,   ob_rash=ob_rash, date_d=self.sl['date_d'], summ= self.sl['summ'], valuta = self.valuta, document= self.sl['document'], uiid_document= self.sl['uiid_document'])
    try:
      h.full_clean()
    except ValidationError as e:
      self.resp = self.otvet('error history')
      return False
    h.save()
    self.resp = self.otvet('ok')
    return True

  def zapisSv(self):
      vid_svyzi = 'org'
      osn = self.findUIID('osn', 'debitor')
      if osn is None:
        self.resp = self.otvet('debitor')
        return False
      sv = self.findUIID('sv', 'debitor')
      if sv is None:
        self.resp = self.otvet('debitor')
        return False
      ll = SvLitsa(vid_svyzi=vid_svyzi, osn=osn, sv = sv)
      try:
        ll.full_clean()
      except ValidationError as e:
        self.resp = self.otvet('error sv')
        return False
      ll.save()
      self.resp = self.otvet('ok')
      return True

  def zapisAcc(self):
      share = self.sl['share']
      vlad = self.findUIID('vlad', 'debitor')
      if vlad is None:
        self.resp = self.otvet('debitor')
        return False
      doch = self.findUIID('doch', 'debitor')
      if doch is None:
        self.resp = self.otvet('debitor')
        return False
      try:
        ll , is_create = Acc.objects.update_or_create(vlad=vlad, doch = doch)
        ll.share = share
        ll.save()
      except ValidationError as e:
        self.resp = self.otvet('error acc')
        return False
      self.resp = self.otvet('ok')
      return True

  def delDolg(self):
    Dolg.objects.filter(id_company=self.company, uiid_dolg= self.sl['uiid_dolg']).delete()

  def delDvj(self):
    Dvj.objects.filter(id_company=self.company, uiid_document= self.sl['uiid_document']).delete()

  def ZapisDog(self):
    q = OutputId.objects.filter(id_company= self.company, uiid= self.sl['uiid'], dogovor__isnull = False)
    if q.count()==1:
      dd = q[0].dogovor
    else:
      dd = None

    kreditor = self.findUIID('uiid_k', 'debitor')
    if kreditor is None:
      self.resp = self.otvet('kreditor')
      return False
    debitor = self.findUIID('uiid_d','debitor')
    if debitor is None:
      self.resp = self.otvet('debitor')
      return False
    if not self.findValuta():
      return False
    if dd is not None:
      dd.debitor = debitor
      dd.kreditor = kreditor
      dd.valuta = valuta
      dd.title = self.sl['tt']
      dd.date = self.sl['dd']
      dd.date_e = self.sl['de']
    else:
      dd = Dogovor(id_company= self.company, kreditor=kreditor, debitor=debitor, valuta = valuta, title= self.sl['tt'], date= self.sl['dd'] , date_e=self.sl['de'] , uiid = self.sl['uiid'])
    try:
        dd.full_clean()
    except ValidationError as e:
        self.resp = self.otvet('error dog')
        return False
    dd.save()
    try:
      out, is_create = OutputId.objects.update_or_create(id_company= self.company, uiid= self.sl['uiid'], dogovor= dd)
    except ValidationError as e:
      self.resp = self.otvet('error out')
      return False
    self.resp = self.otvet('ok')
    return True




  def ZapisObRash(self):
    q = OutputId.objects.filter(id_company= self.company, uiid= self.sl['uiid'], ob_rash__isnull= False)
    if q.count()==1:
       dd = q[0].ob_rash
    else:
       dd = None

    kreditor = self.findUIID('uiid_k', 'debitor')
    if kreditor is None:
      self.resp = self.otvet('kreditor')
      return False
    debitor = self.findUIID('uiid_d','debitor')
    if debitor is None:
      self.resp = self.otvet('debitor')
      return False

    if dd is not None:
      dd.debitor = debitor
      dd.kreditor = kreditor
      dd.title = self.sl['tt']
    else:
      dd = ObRash(id_company= self.company, kreditor=kreditor, debitor=debitor, title= self.sl['tt'] , uiid = self.sl['uiid'])
    try:
        dd.full_clean()
    except ValidationError as e:
        self.resp = self.otvet('error ob_rash')
        return False
    dd.save()
    try:
      out, is_create = OutputId.objects.update_or_create(id_company= self.company, uiid= self.sl['uiid'], ob_rash= dd)
    except ValidationError as e:
      self.resp = self.otvet('error out')
      return False
    self.resp = self.otvet('ok')
    return True



  def obrabotka(self):

      if self.sl['p'] == 'dolg':
        self.delDolg()
        # нужен цикл по всем долгам
        self.zapisDolg()
      elif self.sl['p'] == 'debitor':
        self.zapisDebitor()
      elif self.sl['p'] == 'dvj':
        self.delDvj()
        # движения в цикле
        self.zapisDvj()
      elif self.sl['p'] == 'org':
        self.zapisSv()
      elif self.sl['p'] == 'acc':
        self.zapisAcc()
      elif self.sl['p'] == 'dog':
        self.zapisDog()
      elif self.sl['p'] == 'ob_rash':
        self.zapisObRash()
      else:
        self.resp= self.otvet('Metod POST ne opredelen')
