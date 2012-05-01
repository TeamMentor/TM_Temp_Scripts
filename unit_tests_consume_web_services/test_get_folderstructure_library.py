import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_folderstructure_library():
  a=client.service.GetFolderStructure_Library('4738d445-bc9b-456c-8b35-a35057596c16')
  match=re.search(r'^\(Library_V3\)\{\s+libraryId\s=\s\"[\w-]*\"\s+name\s=\s\"[\w\s]*\"\s+subFolders\s=\s+.*views\s=.*libraryId\s=[\"\w-]*\s+.*guid\[\]\s=\s+\"[\w-]*\".*\}$',str(a),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_folderstructure_library():
  assert get_folderstructure_library() == 'true'
