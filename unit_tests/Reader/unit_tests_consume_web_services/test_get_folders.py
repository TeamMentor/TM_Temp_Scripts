import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_folders():
  #client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  guid=client.service.GetFolders('4738d445-bc9b-456c-8b35-a35057596c16')
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\"\s+name\s=\s\".*\"\s+views\s=',str(guid),re.DOTALL)
  #client.service.Logout()
  if match:
    return 'true'

def test_get_folders():
  assert get_folders() == 'true'
