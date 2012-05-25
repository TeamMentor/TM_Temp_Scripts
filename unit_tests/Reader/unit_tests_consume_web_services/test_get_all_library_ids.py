import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_libraryids():
  i=0
  #client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
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
