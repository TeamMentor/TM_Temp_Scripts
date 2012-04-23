import suds
import re
import sys
import os

#Enter WSDL Url here
url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'

#All Global variables
users={}; datatype_values={}; report={}

def main():
  #Connect to website and retrieve object which contains WSDL details
  client=connect(url)

  #Get usernames and password of the users you need to login with from a file. This file needs to be manually filled in with data in a userTABpassword format.
  users=get_users_passwords()

  #Many web service methods have parameters; each of which needs a value of a specific format. Read sample values for all possible datatypes from a file.
  #This file too has to be prefilled in a datatypeTABsample value format.
  get_sample_values_datatypes()

  #Get exact list of all methods exported by the Webservice.
  methods=get_methods_parameters_datatypes(client)

  #Who are the attackers for each method? Who can query but are NOT supposed to query each method? Fill up a list of attackers per method. We haven't yet started
  #any querying though
  methods=map_adversaries_to_methods(methods)

  #Login as each potential adversary and query each method. The results are written into a CSV file.
  report=analysis(client,users,methods)

  #Create report after analysis is complete.
  create_report(report)

def connect(url):
  #Use the Suds library to connect and return an object which is used later to query individual methods.
  client = suds.client.Client(url)
  return client

def get_users_passwords():
  try:
    f=open('users','rU')
  except:
    print 'Could not find file containing usernames and passwords'

  #Read users from file, create a hash which has the username as the key and the password as the value.
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\s+$',r'',t1[1])
    users[t1[0]]=t1[1]
  f.close()

  return users

def get_sample_values_datatypes():
  try:
    f=open('datatype_sample_value_mapping','rU')
  except:
    print 'Could not find file containing mapping between datatypes and values'

  #Read datatypes and sample values for each from a file on disk; create a hash where the datatype is the key and the sample value is the value.
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\s+$',r'',t1[1])
    datatype_values[t1[0]]=t1[1]
  f.close()

def get_methods_parameters_datatypes(client):
  #Remember the client object we got initially? We parse that object here to retrieve only all the Web Service methods.
  t1=re.findall(r'.*Methods\ \(\d+\)(.*)Types\ \(\d+\)',str(client),re.DOTALL)
  t3=t1[0].split('\n')

  #Do a little beautification :)
  methods={}
  for i in t3:
    t2=re.sub(r'^\s*',r'',i)
    if re.search(r'^\w',t2):
      methods[t2]=''

  #.....and return a hash which contains all methods as keys. All keys have blank values.
  return methods

def map_adversaries_to_methods(methods):
  manual_action_adversary_map={}
  try:
    f=open('method_attacker_mapping','rU')
  except:
    print 'Could not open file containing Method & Attacker mapping'

  #Read Method attacker mapping from file and fill up the hash which contained only all methods as keys with potential attackers for each method. This bit is 
  #filling a temp hash up.
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\n$',r'',t1[1])
    manual_action_adversary_map[t1[0]]=t1[1]

  #...and now the data from the temp hash is used to fill up the real hash.
  for key in methods.keys():
    t2=key.split('(')
    if t2[0] in manual_action_adversary_map:
      methods[key]=manual_action_adversary_map[t2[0]]

  #...and the filled up hash is returned.
  return methods

def analysis(client,users,methods):
  #This is a list of methods which just don't work...even without the script, when queried manually using something like SoapUI
  ignored_methods = ['GetAllGuidanceItems()','GitHub_Push_Origin()','Logout()','GetAllUserLogs()','GetDeletedLibraries()','GitHub_Push_Commit()','DeleteDeletedGuidanceTypes()','DeleteDeletedLibraries()','GitHub_Pull_Origin()','GetGuidanceTypes()','GetGuidanceTypes()','GetGuidanceTypes()','GetUploadToken()','GetGuidanceItemsInViews(ArrayOfGuid viewIds, )','JsDataTableWithGuidanceItemsInViews(ArrayOfGuid viewIds, )','UpdateLibrary(ns1:Library library, )','CreateLibrary(ns1:Library library, )','CreateArticle(TeamMentor_Article article, )','CreateUsers(ArrayOfNewUser newUsers, )','CreateGuidanceItem(GuidanceItem_V3 guidanceItem, )']

  #For each attacker
  for key in users.keys():
    #Just to track progress on your screen
    print "User -- " + key

    #Set a proxy if you want; I wanted to look at responses for each request so I passed it through Burp
    d = dict(http='127.0.0.1:8080')
    client.set_options(proxy=d)

    #You need to 'login' only if you're an anonymous user
    if key != 'anonymous':
      client.service.Login(key,users[key])
      #Is a proper session created and stored in my cookie jar?
      match = re.search(r'ASP.NET_SessionId=.*Cookie Session=', str(client.options.transport.cookiejar))
      if match:
        #CSRF Token needed for each request; grab that
        user_properties=client.service.Current_User()
        client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
  
    #Analyze method which have no additional parameters. For e.g TMConfigFile()
    analysis_methods_no_params(f,key,client,methods,ignored_methods)

    #Analyze methods that have one or more parameters. For e.g XmlDatabase_GetGuidanceItemXml(ns0:guid guidanceItemId, )
    report=analysis_methods_params(f,key,client,methods,ignored_methods)

  #Once done with ALL methods for that user, you logout and go back to the next user.
  client.service.Logout()

  #Pass on your results to the reporting function :)
  return report

def analysis_methods_no_params(f,key,client,methods,ignored_methods):
  for method in methods.keys():
    if not method in ignored_methods:
      try:
        t2=methods[method].split(',')
        #Identify 'parameterless' methods and invoke each of them
        if re.search(r'\(\)',method) and key in t2:
          b=eval('client.service.'+method)
          report[key+'^'+method+'^'+'OK\n']=''
      except Exception:
        #Code reaches here only if eval fails; we want to track why..hence sys.exc_info()
        exc_type, exc_value = sys.exc_info()[:2]
        t1=str(exc_value).split('\n')
        report[key+'^'+method+'^'+t1[0]+'\n']=''
        #Continues with the next iteration irrespective of the exception thrown
        pass

def analysis_methods_params(f,key,client,methods,ignored_methods):
  for method in methods.keys():
    i=0;l1='';t1='';t2=''
    if not method in ignored_methods:
      try:
        t2=methods[method].split(',')
        #Identify 'parameter' methods and invoke each of them
        if not re.search(r'\(\)',method) and key in t2:
          t1=re.search(r'(.*)\((.*)\).*',method)
          params=t1.group(2).split(',')
          #Constructing the exact string to call using eval
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
          #Contains complete final string, which is then called
          x='client.service.'+t1.group(1)+'('+l1+')'
          b=eval(x)
          report[key+'^'+method+'^'+'OK\n']=''
      except Exception:
        #Code reaches here only if eval fails; we want to track why..hence sys.exc_info()
        exc_type, exc_value = sys.exc_info()[:2]
        t4=str(exc_value).split('\n')
        #Continues with the next iteration irrespective of the exception thrown
        report[key+'^'+method+'^'+t4[0]+'\n']=''
        pass

  return report

def create_report(report):
  #Remove old reports file
  os.remove('report.csv')

  #Create new reports file and write analysis to it
  f=open('report.csv','w')
  f.write('Attacker'+'^'+'Web service function name'+'^'+'Exceptions if any\n')
  for key in report.keys():
    f.write(key)
  f.close()

main()
