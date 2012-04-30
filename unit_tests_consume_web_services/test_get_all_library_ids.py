import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_libraryids():
  i=0
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.GetAllLibraryIds()
  while i < len(guid):
    match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',str(guid[i]))
    if not match:
      #client.service.Logout()
      return 'false'
      break
    i+=1

  #client.service.Logout()
  return 'true'

def test_get_all_libraryids():
  assert get_all_libraryids() == 'true'
