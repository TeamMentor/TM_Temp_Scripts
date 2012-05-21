import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_view_by_id():
  a=client.service.GetViewById('d09a1340-a411-4b53-8f24-520dc8d5abb9')
  m1=re.search(r'^\(View.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\".*viewId\s=\s\"[\w-]*\".*caption\s=\s\".*\"\s+guidanceItems\s=\s+.*guid\[\]\s=\s+\"[\w-]*\"',str(a),re.DOTALL)
  if m1:
    return 'true'

def test_get_view_by_id():
  assert get_view_by_id() == 'true'
