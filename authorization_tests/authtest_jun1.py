import suds
import re
import sys
import os
import datetime
from lxml import etree

#Enter WSDL Url here
url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'

#All Global variables
users={}; stored_responses={}; method_correct_value={};report={}
response_dir='auth_testing_responses/';
report_dir='auth_testing_reports/'

def main():
  #Connect to website and retrieve object which contains WSDL details
  client=connect(url)

  #Get usernames and password of the users you need to login with from a file. This file needs to be manually filled in with data in a userTABpassword format
  users=get_users_passwords()

  #Get exact list of all methods exported by the Webservice.
  methods=get_methods_parameters_datatypes(client)

  #Who are the attackers for each method? Who can query but are NOT supposed to query each method? Fill up a list of attackers per method. We haven't yet started any querying though
  methods=map_adversaries_to_methods(methods)

  #Login as each potential adversary and query each method
  responses=invoke_methods(client,users,methods)

  #Generate XML from received responses
  xml_responses=generate_xml_response(stored_responses)

  #Analyze XML responses and store analysis in hash
  report=analysis(xml_responses,methods)

  #Generate final report in XML format from hash
  create_report(report)


#Connect and retrieve WSDL
def connect(url):
  #Use the Suds library to connect and return an object which is used later to query individual methods.
  client = suds.client.Client(url)
  d = dict(http='127.0.0.1:8080')
  client.set_options(proxy=d)
  return client

#Get all user credentials
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

#Get all methods
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

#Who is allowed to access what?
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

    #Added expected value code
    t1[2]=re.sub(r'\n$',r'',t1[2])
    method_correct_value[t1[0]]=t1[2]

  #...and now the data from the temp hash is used to fill up the real hash.
  for key in methods.keys():
    t2=key.split('(')
    if t2[0] in manual_action_adversary_map:
      methods[key]=manual_action_adversary_map[t2[0]]

  #...and the filled up hash is returned.
  return methods

def wsmethod_rbac_has_role(key,client):
  resp=client.service.RBAC_HasRole('ReadArticles')
  stored_responses['RBAC_HasRole:'+key]=resp

def wsmethod_rbac_current_identity_auth(key,client):
  resp=client.service.RBAC_CurrentIdentity_IsAuthenticated()
  stored_responses['RBAC_CurrentIdentity_IsAuthenticated:'+key]=resp

#Invoke every web service method for every single user
def invoke_methods(client,users,methods):
  for key in users.keys():
    if str(key) != 'anonymous':
      guid=client.service.Login(key,users[key])
      match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
      if match:
        user_properties=client.service.Current_User()
        client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
        call_all_webservice_methods(key,client)
        client.service.Logout()
    else:
        key='anonymous'
        call_all_webservice_methods(key,client)

  return stored_responses

#Wrapper to call each and every web service method
def call_all_webservice_methods(key,client):
  wsmethod_rbac_has_role(key,client)
  wsmethod_rbac_current_identity_auth(key,client)

#Where do I store the response?
def get_response_path():
  response_path=response_dir+__file__[0:-2]+str(datetime.datetime.now())+'.xml'
  return response_path

#Where do I store the reports?
def get_report_path():
  report_path=report_dir+__file__[0:-2]+str(datetime.datetime.now())+'.xml'
  return report_path

#Write XML responses to file
def generate_xml_response(responses):
  path=get_response_path()
  root = etree.Element("Test", name='Authorization Test')
  for key in stored_responses.keys():
    method_user = etree.SubElement(root,"Method_and_User", method_user=str(key))
    method_user.text = str(stored_responses[key])

  t1 = etree.ElementTree(root)
  t1.write(path, pretty_print=True)
  return path

#Analyze stored responses
def analysis(xmlresponse,methods):
  map1={}
  for m1 in methods:
    t1=m1.split('(')
    map1[t1[0]]=methods[m1]

  tree = etree.parse(xmlresponse)
  root = tree.getroot()
  for child in root.iterchildren():
    attributes=child.attrib
    t1=attributes['method_user'].split(':')
    if t1[0] in map1:
      t2=map1[t1[0]].split(',')
      if t1[1] not in t2:
        report[t1[0]]=t1[1]

  return report

#Create XML report after analysis
def create_report(report):
  path=get_report_path()
  root = etree.Element("Test", name='Authorization Test')
  if report.keys():
     for key in report.keys():
       method = etree.SubElement(root,"Method", method=str(key))
       method.text = str(report[key])
  else:
    root.text='No authorization loopholes at all'

  t1 = etree.ElementTree(root)
  t1.write(path, pretty_print=True)
  return path

#Code starts running here
main()
