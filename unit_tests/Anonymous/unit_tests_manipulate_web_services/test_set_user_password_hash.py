import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def set_user_password_hash():
  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.SetUserPasswordHash(402151848,'23972ba7370450a08aacf086630bb6e650b530cc625c13d1556b2d641bfb3675')
    if str(a) == 'True':
      client.service.Logout()
      return 'true'

def test_set_user_password_hash():
  assert set_user_password_hash() == 'true'
