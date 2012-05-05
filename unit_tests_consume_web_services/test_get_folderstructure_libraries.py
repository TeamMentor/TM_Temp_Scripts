import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_folderstructure_libraries():
  a=client.service.GetFolderStructure_Libraries()
  match=re.search(r'^\(ArrayOfLibrary_V3\)\{\s+Library_V3\[\]\s=\s+\(Library_V3\)\{\s+libraryId\s=\s\"[\w-]*\"\s+name\s=\s\"[\w\s]*\"\s+subFolders\s=\s+.*views\s=.*libraryId\s=[\"\w-]*\s+.*guid\[\]\s=\s+\"[\w-]*\".*\}$',str(a),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_folderstructure_libraries():
  assert get_folderstructure_libraries() == 'true'
