import suds
import re

url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'

def login():
  client = suds.client.Client(url)
  guid=client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)

  if match:
    return 'true'

def logout():
  client = suds.client.Client(url)
  client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  guid=client.service.Logout()
  match=re.search(r'(0{8})-0{4}-0{4}-0{4}-0{12}',guid)

  if match:
    return 'true'

def test_login_and_logout():
  assert login() == 'true'
  assert logout() == 'true'
