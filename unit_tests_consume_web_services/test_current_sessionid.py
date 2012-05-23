import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_current_session_id():
    a=client.service.Current_SessionID()
    m1=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',str(a))
    if m1:
      client.service.Logout()
      return 'true'

def test_get_current_session_id():
  assert get_current_session_id() == 'true'
