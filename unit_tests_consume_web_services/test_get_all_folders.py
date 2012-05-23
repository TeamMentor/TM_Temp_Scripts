import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_all_folders():
  a=client.service.GetAllFolders()
  m1=re.search(r'\(ArrayOfFolder_V3\)\{\s+Folder_.*\[\]\s\=\s+\(Folder.*\{\s+',str(a),re.DOTALL)
  if m1:
    client.service.Logout()
    return 'true'

def test_get_all_folders():
  assert get_all_folders() == 'true'
