from lxml import etree
import datetime

response_dir='auth_testing_responses/';
report_dir='auth_testing_reports/'

#Write XML responses to file
def generate_xml_response(stored_responses):
  path=get_response_path()
  #Construct the response to be written
  root = etree.Element("Test", name='Authorization Test')
  for key in stored_responses.keys():
    method_user = etree.SubElement(root,"Method_and_User", method_user=str(key))
    method_user.text = str(stored_responses[key])

  #Write the response
  t1 = etree.ElementTree(root)
  t1.write(path, pretty_print=True)
  return path

#Create XML report after analysis
def create_report(report):
  path=get_report_path()
  #Construct the report
  root = etree.Element("Test", name='Authorization Test')
  if report.keys():
     for key in report.keys():
       method = etree.SubElement(root,"Method", method=str(key))
       method.text = str(report[key])
  else:
    root.text='No authorization loopholes at all'

  #Write the report
  t1 = etree.ElementTree(root)
  t1.write(path, pretty_print=True)
  return path

#Where do I store the response?
def get_response_path():
  response_path=response_dir+'response_'+str(datetime.datetime.now())+'.xml'
  return response_path

#Where do I store the reports?
def get_report_path():
  report_path=report_dir+'report_'+str(datetime.datetime.now())+'.xml'
  return report_path
