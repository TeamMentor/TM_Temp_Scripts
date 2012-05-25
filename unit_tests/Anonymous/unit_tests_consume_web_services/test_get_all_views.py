import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_views():
  #
  guid=client.service.GetAllViews()
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\".*viewId\s=\s\"[\w-]*\".*caption\s=\s\".*\"\s+guidanceItems\s=\s+.*guid\[\]\s=\s+\"[\w-]*\"',str(guid),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_all_views():
  assert get_all_views() == 'true'
