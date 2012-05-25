import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_library_by_name():
  guid=client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.GetLibraryByName('arsenalFC')
    m1=re.search(r'\(Library\)\{\s+_caption\s=\s\"',str(a),re.DOTALL)
    if m1:
      client.service.Logout()
      return 'true'

def test_get_library_by_name():
  assert get_library_by_name() == 'true'
