import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_views():
  #client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  guid=client.service.GetAllViews()
  match=re.search(r'^\(ArrayOf.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\".*viewId\s=\s\"[\w-]*\".*caption\s=\s\".*\"\s+guidanceItems\s=\s+.*guid\[\]\s=\s+\"[\w-]*\"',str(guid),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_all_views():
  assert get_all_views() == 'true'
