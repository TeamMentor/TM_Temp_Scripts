import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def logout():
  client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.Logout()
  match=re.search(r'(0{8})-0{4}-0{4}-0{4}-0{12}',guid)
  if match:
    return 'true'

def test_logout():
  assert logout() == 'true'
