import suds
import sys
import os
import re
import datetime
from lxml import etree

payloads=[]; responses={}

met = 'GetUser_byName'
payload_dir='payloads/'
url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'

client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

#Login before invoking anything
def login():
  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    return 'true'
  else:
    return 'false'

#Where do I store the response?
def get_response_path():
  response_path='responses/'+__file__[0:-2]+str(datetime.datetime.now())+'.xml'
  return response_path

#Actual web service method invoking; only 1st 300 characters of the response stored
def get_user_by_name(list_payload):
  for i in list_payload:
    try:
      a=client.service.GetUser_byName(i)
      print i
      responses[i]=str(a)[0:300]
    except Exception:
      exc_type, exc_value = sys.exc_info()[:2]
      responses[i]=str(exc_value)[0:300]
      pass
  return responses

#Open config file and get a list of all files which have payloads in them; expand them and store them in the payloads 'list'
def get_payloads():
  f=open('method_payload_config','r')
  for i in f:
    i=re.sub(r'\n$',r'',i)
    m1=re.search(met,i)
    if m1:
      t1=i.split(':')
      payload_files=t1[1].split(',')
  f.close()

  for file in payload_files:
    f=open(payload_dir+file,'r')
    for payload in f:
      payload=re.sub(r'\n$',r'',payload)
      payloads.append(payload)
    f.close()

  return payloads

#Its all done here; just have to write
def generate_xml(responses):
  path=get_response_path()
  root = etree.Element("Method", name=met)
  for key in responses.keys():
    payload = etree.SubElement(root,"Payload")
    payload.text = key
    resp = etree.SubElement(payload,"Response")
    resp.text = responses[key]

  t1 = etree.ElementTree(root)
  t1.write(path, pretty_print=True)

def main():
  #Login to invoke the WS
  is_logged_in=login()

  #If Login successful
  if is_logged_in == 'true':
    #Get a list of all valid payloads for this method
    list_payload=get_payloads()
    #Invoke method with each payload; one by one; responses all stored in a payload-response hash
    responses=get_user_by_name(list_payload)
    #Write results to XML
    report=generate_xml(responses)
    #Logout
    client.service.Logout()
  else:
    sys.exit(0)

main()
