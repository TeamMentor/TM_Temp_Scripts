import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def xml_Database_GuidanceItems_SearchTitleAndHtml():
  guid=client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    guidanceitem=client.factory.create('ArrayOfGuid')
    guidanceitem['guid'] = ["f634adbd-f54d-421f-9d6d-e208b8acbf84","00000000-0000-0000-0000-000000466605","10000000-0000-0000-0000-000000000000"]
    searchtext = 'googoo'
    a=client.service.XmlDatabase_GuidanceItems_SearchTitleAndHtml(guidanceitem, searchtext)
    m1=re.search(r'\(ArrayOfGuid\)\{\s+guid\[\]\s=\s+["\-\d]+',str(a),re.DOTALL)
    if m1:
      client.service.Logout()
      return 'true'

def test_xml_Database_GuidanceItems_SearchTitleAndHtml():
  assert xml_Database_GuidanceItems_SearchTitleAndHtml() == 'true'
