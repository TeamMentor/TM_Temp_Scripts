import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsDataTableWithGuidanceItemsInViews():
  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.JsDataTableWithGuidanceItemsInViews('d09a1340-a411-4b53-8f24-520dc8d5abb9')
    match=re.search(r'\(JsDataTable\)\{\s+aaData\s=\s.*aoColumns\s=\s',str(a),re.DOTALL)
    if match:
      client.service.Logout()
      return 'true'

def test_JsDataTableWithGuidanceItemsInViews():
  assert JsDataTableWithGuidanceItemsInViews() == 'true'
