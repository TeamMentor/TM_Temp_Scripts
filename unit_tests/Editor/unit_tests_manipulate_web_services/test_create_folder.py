import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def create_folder():
  guid=client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.CreateFolder('4738d445-bc9b-456c-8b35-a35057596c16','00000000-0000-0000-0000-000000000000','fyiboo')
    m1=re.search(r'\(Folder.*\{\s+libraryId\s=\s\"[\w-]*\"',str(a),re.DOTALL)
    if m1:
      client.service.Logout()
      return 'true'

def test_create_folder():
  assert create_folder() == 'true'
