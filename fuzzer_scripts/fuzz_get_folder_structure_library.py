import suds
import sys
import os
import re
import datetime

payloads=[]
url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_response_path():
  response_path='responses/'+__file__+'_'+str(datetime.datetime.now())
  return response_path

def get_folderstructure_library(list_payload):
  path=get_response_path()
  f=open(path,'w')
  for i in list_payload:
    f.write('\n\n'+'='*60+str(i)+'='*60+'\n\n')
    try:
      a=client.service.GetFolderStructure_Library(str(i))
      f.write(str(a)[0:300])
    except Exception:
      exc_type, exc_value = sys.exc_info()[:2]
      f.write(str(exc_value)[0:300])
      pass
  f.close()

def get_payloads():
  f=open('guid_payloads','r')
  for payload in f:
    payload=re.sub(r'\n$',r'',payload)
    payloads.append(payload)
  f.close()
  return payloads

def main():
  list_payload=get_payloads()
  get_folderstructure_library(list_payload)

main()
