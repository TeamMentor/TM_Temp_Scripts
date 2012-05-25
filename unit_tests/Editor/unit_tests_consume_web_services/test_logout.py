import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def logout():
  client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  guid=client.service.Logout()
  match=re.search(r'(0{8})-0{4}-0{4}-0{4}-0{12}',guid)
  if match:
    return 'true'

def test_logout():
  assert logout() == 'true'
