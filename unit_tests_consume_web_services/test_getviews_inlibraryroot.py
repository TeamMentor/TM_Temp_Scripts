import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def getviews_inlibraryroot():
  a=client.service.GetViewsInLibraryRoot('10000000-0000-0000-0000-000000000006')
  match=re.search(r'^\(ArrayOfView.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\"\s+viewId\s=\s\".*\"\s+caption\s=',str(a),re.DOTALL)
  if match:
    return 'true'

def test_getviews_inlibraryroot():
  assert getviews_inlibraryroot() == 'true'
