import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def test_get_all_views():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.GetAllViews()
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\".*viewId\s=\s\"[\w-]*\".*caption\s=\s\".*\"\s+guidanceItems\s=\s+.*guid\[\]\s=\s+\"[\w-]*\"',str(guid),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'
