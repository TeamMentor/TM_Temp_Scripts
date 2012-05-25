import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_folders():
  #client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  guid=client.service.GetFolders('4738d445-bc9b-456c-8b35-a35057596c16')
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\"\s+name\s=\s\".*\"\s+views\s=',str(guid),re.DOTALL)
  #client.service.Logout()
  if match:
    return 'true'

def test_get_folders():
  assert get_folders() == 'true'
