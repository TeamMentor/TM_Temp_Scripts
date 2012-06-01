import suds
import sys
import os
import re
import datetime
from lxml import etree
import threading

payloads=[]; responses={}; method_exp_values={}; report={}

met = 'RBAC_HasRole'
payload_dir='payloads/'; response_dir='responses/'; report_dir='reports/'
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
  response_path=response_dir+__file__[0:-2]+str(datetime.datetime.now())+'.xml'
  return response_path

#Where do I store the report?
def get_report_path():
  report_path=report_dir+__file__[0:-2]+str(datetime.datetime.now())+'.xml'
  return report_path

#Actual web service method invoking; only 1st 300 characters of the response stored
def rbac_has_role(list_payload):
  threads=[]
  for i in list_payload:
    #Start a new thread for each payload
    t = threading.Thread(target=thread_rbac_has_role, args=(i,))
    threads.append(t)
    t.start()
    #responses=thread_rbac_has_role(i)
  return responses

#Each thread invokes a method
def thread_rbac_has_role(payload):
    try:
      a=client.service.RBAC_HasRole(payload)
      responses[payload]=str(a)
      return responses
    except Exception:
      exc_type, exc_value = sys.exc_info()[:2]
      responses[payload]=str(exc_value)
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
  return path

#Get expected return values after fuzz; this is both success and failure
def get_expected_values():
  f=open('method_expected_values','r')
  for i in f:
    t1=i.split(':')
    method_exp_values[t1[0]]=t1[1]
  f.close()
  return method_exp_values

#Analyze responses obtained after fuzzing
def analysis_xml(xmlresponse):
  payload_size_map = {}
  tree = etree.parse(xmlresponse)
  root = tree.getroot()
  for child in root.iterchildren():
    for gc in child.iterchildren():
      if str(gc.tag) == 'Response':
        if met in method_exp_values:
          method_exp_values[met] = re.sub(r'\n$',r'',method_exp_values[met])
          t1=method_exp_values[met].split(',')
          if str(gc.text) not in t1:
            report[str(child.text)] = 'Unexpected response generated '+str(gc.text)

  return report

def generate_xml_report(report):
  if report.keys():
     path=get_report_path()
     root = etree.Element("Method", name=met)
     for key in report.keys():
       payload = etree.SubElement(root,"Payload")
       payload.text = key
       resp = etree.SubElement(payload,"Result")
       resp.text = report[key]

     t1 = etree.ElementTree(root)
     t1.write(path, pretty_print=True)
     return path

def main():
  #Login to invoke the WS
  is_logged_in=login()

  #If Login successful
  if is_logged_in == 'true':
    #Get a list of all valid payloads for this method
    list_payload=get_payloads()
    #Get a list of all expected values for this method
    method_exp_values=get_expected_values()
    #Invoke method with each payload; one by one; responses all stored in a payload-response hash
    responses=rbac_has_role(list_payload)
    #Write results to XML
    xmlresponse=generate_xml(responses)
    #Analyze XML results
    report=analysis_xml(xmlresponse)
    #Generate XML report
    generate_xml_report(report)
    #Logout
    client.service.Logout()
  else:
    sys.exit(0)

main()
