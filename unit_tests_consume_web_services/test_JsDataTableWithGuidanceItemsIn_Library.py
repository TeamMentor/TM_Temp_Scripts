import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsDataTableWithGuidanceItemsIn_Library():
  a=client.service.JsDataTableWithGuidanceItemsIn_Library('10000000-0000-0000-0000-000000000006')
  match=re.search(r'\(JsDataTable\)\{\s+aaData\s=\s.*aoColumns\s=\s',str(a),re.DOTALL)
  if match:
    return 'true'

def test_JsDataTableWithGuidanceItemsIn_Library():
  assert JsDataTableWithGuidanceItemsIn_Library() == 'true'
