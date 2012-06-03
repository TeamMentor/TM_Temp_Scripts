import suds
import re
import sys

users={}

def geturl():
  try:
    f=open('config','rU')
  except:
    print 'Could not find config file'
  config=f.readlines()
  for i in config:
    if 'url' in i:
      t1=i.split('=')
      url=t1[1]
      break

  url=re.sub(r'\s+$',r'',url)
  return url
     
#Connect and retrieve WSDL
def connect(url):
  #Use the Suds library to connect and return an object which is used later to query individual methods.
  client = suds.client.Client(url)
  #Set proxy to the awesome Burp for debugging purposes; uncomment the next 2 lines if you want to look at requests :)
  #d = dict(http='127.0.0.1:8080')
  #client.set_options(proxy=d)
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
