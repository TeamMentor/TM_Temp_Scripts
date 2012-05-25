import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_folders():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.GetFolders('4738d445-bc9b-456c-8b35-a35057596c16')
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\"\s+name\s=\s\".*\"\s+views\s=',str(guid),re.DOTALL)
  #client.service.Logout()
  if match:
    return 'true'

def test_get_folders():
  assert get_folders() == 'true'
