import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_string_indexes():
  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.GetStringIndexes()
    m1=re.search(r'\(ArrayOfString\)\{\s+string\[\]\s=\s+\"',str(a),re.DOTALL)
    if m1:
      client.service.Logout()
      return 'true'

def test_get_string_indexes():
  assert get_string_indexes() == 'true'