import suds
import sys
import os
import re
import datetime
from lxml import etree

payloads=[]; responses={}
met='GetFolderStructure_Library'

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_response_path():
  response_path='responses/'+__file__+'_'+str(datetime.datetime.now())
  return response_path

def get_folderstructure_library(list_payload):
  path=get_response_path()
  for i in list_payload:
    try:
      a=client.service.GetFolderStructure_Library(str(i))
      responses[i]=str(a)[0:300]
    except Exception:
      exc_type, exc_value = sys.exc_info()[:2]
      responses[i]=str(exc_value)[0:300]
      pass
  return responses

def get_payloads():
  f=open('guid_payloads','r')
  for payload in f:
    payload=re.sub(r'\n$',r'',payload)
    payloads.append(payload)
  f.close()
  return payloads

def generate_xml(responses):
  root = etree.Element("Method", name=met)
  for key in responses.keys():
    payload = etree.SubElement(root,"Payload")
    payload.text = key
    resp = etree.SubElement(payload,"Response")
    resp.text = responses[key]

  t1 = etree.ElementTree(root)
  t1.write('resp.xml', pretty_print=True)

def main():
  list_payload=get_payloads()
  responses=get_folderstructure_library(list_payload)
  report=generate_xml(responses)

main()
