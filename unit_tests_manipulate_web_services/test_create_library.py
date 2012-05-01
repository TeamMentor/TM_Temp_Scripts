import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def create_library():
  param = client.factory.create('ns1:Library')
  param._id='10000000-0000-0000-0000-000000000050'; param._caption='footiearsenal'

  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.CreateLibrary(param)
    if a:
      return 'true'

def test_create_library():
  assert create_library() == 'true'
