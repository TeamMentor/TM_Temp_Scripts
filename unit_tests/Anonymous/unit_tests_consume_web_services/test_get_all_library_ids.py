import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_libraryids():
  i=0
  #
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
