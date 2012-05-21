import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def xml_Database_GuidanceItems_SearchTitleAndHtml():
  guidanceitem=client.factory.create('ArrayOfGuid')
  guidanceitem['guid'] = ["f634adbd-f54d-421f-9d6d-e208b8acbf84","00000000-0000-0000-0000-000000466605","10000000-0000-0000-0000-000000000000"]
  searchtext = 'googoo'
  a=client.service.XmlDatabase_GuidanceItems_SearchTitleAndHtml(guidanceitem, searchtext)
  m1=re.search(r'\(ArrayOfGuid\)\{\s+guid\[\]\s=\s+["\-\d]+',str(a),re.DOTALL)
  if m1:
    return 'true'

def test_xml_Database_GuidanceItems_SearchTitleAndHtml():
  assert xml_Database_GuidanceItems_SearchTitleAndHtml() == 'true'
