import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def login():
  
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    client.service.Logout()
    return 'true'

def test_login():
  assert login() == 'true'
