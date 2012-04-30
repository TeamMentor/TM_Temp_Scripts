import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def login():
  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    client.service.Logout()
    return 'true'

def test_login():
  assert login() == 'true'
