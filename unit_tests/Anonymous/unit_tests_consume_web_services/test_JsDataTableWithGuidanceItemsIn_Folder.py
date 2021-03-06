import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsDataTableWithAllGuidanceItemsInFolder():
  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.JsDataTableWithGuidanceItemsIn_Folder('90f22a68-ddf6-4eb5-ab92-aa2351d8aeff')
    match=re.search(r'\(JsDataTable\)\{\s+aaData\s=\s.*aoColumns\s=\s',str(a),re.DOTALL)
    if match:
      client.service.Logout()
      return 'true'

def test_JsDataTableWithAllGuidanceItemsInFolder():
  assert JsDataTableWithAllGuidanceItemsInFolder() == 'true'
