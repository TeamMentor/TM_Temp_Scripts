import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def getviews_inlibraryroot():
  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.GetViewsInLibraryRoot('10000000-0000-0000-0000-000000000006')
    match=re.search(r'^\(ArrayOfView.*\)\{\s+.*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\"\s+viewId\s=\s\".*\"\s+caption\s=',str(a),re.DOTALL)
    if match:
      client.service.Logout()
      return 'true'

def test_getviews_inlibraryroot():
  assert getviews_inlibraryroot() == 'true'
