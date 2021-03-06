import suds
import re
import sys
import os
import traceback

url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'
users={}; datatype_values={}

def main():
  client=connect_and_login(url)
  users=get_users_passwords()
  get_sample_values_datatypes()
  methods=get_methods_parameters_datatypes(client)
  methods=map_adversaries_to_methods(methods)
  report=analysis(client,users,methods)

def connect_and_login(url):
  client = suds.client.Client(url)
  client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match = re.search(r'ASP.NET_SessionId=.*Cookie Session=', str(client.options.transport.cookiejar))
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    return client
  client.service.Logout()

def get_users_passwords():
  f=open('users','rU')
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\s+$',r'',t1[1])
    users[t1[0]]=t1[1]
  f.close()
  return users

def get_sample_values_datatypes():
  f=open('datatype_sample_value_mapping','rU')
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\s+$',r'',t1[1])
    datatype_values[t1[0]]=t1[1]
  f.close()

def get_methods_parameters_datatypes(client):
  t1=re.findall(r'.*Methods\ \(\d+\)(.*)Types\ \(\d+\)',str(client),re.DOTALL)
  t3=t1[0].split('\n')

  methods={}
  for i in t3:
    t2=re.sub(r'^\s*',r'',i)
    if re.search(r'^\w',t2):
      methods[t2]=''

  return methods

def map_adversaries_to_methods(methods):
  manual_action_adversary_map={}
  f=open('method_attacker_mapping','rU')
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\n$',r'',t1[1])
    manual_action_adversary_map[t1[0]]=t1[1]

  for key in methods.keys():
    t2=key.split('(')
    if t2[0] in manual_action_adversary_map:
      methods[key]=manual_action_adversary_map[t2[0]]

  return methods

def analysis(client,users,methods):
  ignored_methods = ['GetAllGuidanceItems()','GitHub_Push_Origin()','Logout()','GetAllUserLogs()','GetDeletedLibraries()','GitHub_Push_Commit()','DeleteDeletedGuidanceTypes()','DeleteDeletedLibraries()','GitHub_Pull_Origin()','GetGuidanceTypes()','GetGuidanceTypes()','GetGuidanceTypes()','GetUploadToken()','GetGuidanceItemsInViews(ArrayOfGuid viewIds, )','JsDataTableWithGuidanceItemsInViews(ArrayOfGuid viewIds, )','UpdateLibrary(ns1:Library library, )','CreateLibrary(ns1:Library library, )','CreateArticle(TeamMentor_Article article, )','CreateUsers(ArrayOfNewUser newUsers, )','CreateGuidanceItem(GuidanceItem_V3 guidanceItem, )']

  os.remove('report.csv')
  for key in users.keys():
    print "User -- " + key
    d = dict(http='127.0.0.1:8080')
    client.set_options(proxy=d)
    client.service.Login(key,users[key])
    match = re.search(r'ASP.NET_SessionId=.*Cookie Session=', str(client.options.transport.cookiejar))
    if match:
      user_properties=client.service.Current_User()
      client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})

      analysis_methods_no_params(key,client,methods,ignored_methods)
      analysis_methods_params(key,client,methods,ignored_methods)

def analysis_methods_no_params(key,client,methods,ignored_methods):
  f=open('report.csv','a')
  f.write('Attacker'+'^'+'Web service function name'+'^'+'Exceptions if any\n')
  for method in methods.keys():
    if not method in ignored_methods:
      try:
        t2=methods[method].split(',')
        if re.search(r'\(\)',method) and key in t2:
          b=eval('client.service.'+method)
          f.write(key+'^'+method+'^'+'OK\n')
      except Exception:
        exc_type, exc_value = sys.exc_info()[:2]
        t1=str(exc_value).split('\n')
        f.write(key+'^'+method+'^'+t1[0]+'\n')
        pass
  f.close()

def analysis_methods_params(key,client,methods,ignored_methods):
  f=open('report.csv','a')
  for method in methods.keys():
    i=0;l1='';t1='';t2=''
    if not method in ignored_methods:
      try:
        t2=methods[method].split(',')
        if not re.search(r'\(\)',method) and key in t2:
          #print method
          t1=re.search(r'(.*)\((.*)\).*',method)
          params=t1.group(2).split(',')
          while i<len(params)-1:
              m=re.search(r'(.*)\s.*',params[i])
              m1=re.sub(r'\s+$',r'',m.group(1))
              m1=re.sub(r'^\s+',r'',m.group(1))
              if m1 in datatype_values:
                params[i] = datatype_values[m1]
                l1=l1+params[i]+','
                i+=1
              else:
                i+=1
          x='client.service.'+t1.group(1)+'('+l1+')'
          b=eval(x)
          f.write(key+'^'+method+'^'+'OK\n')
      except Exception:
        exc_type, exc_value = sys.exc_info()[:2]
        t4=str(exc_value).split('\n')
        f.write(key+'^'+method+'^'+t4[0]+'\n')
        pass
  f.close()
  client.service.Logout()

main()
