import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsDataTableWithAllGuidanceItemsInFolder():
  a=client.service.JsDataTableWithGuidanceItemsIn_Folder('90f22a68-ddf6-4eb5-ab92-aa2351d8aeff')
  match=re.search(r'\(JsDataTable\)\{\s+aaData\s=\s.*aoColumns\s=\s',str(a),re.DOTALL)
  if match:
    return 'true'

def test_JsDataTableWithAllGuidanceItemsInFolder():
  assert JsDataTableWithAllGuidanceItemsInFolder() == 'true'
