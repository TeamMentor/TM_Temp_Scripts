import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_library_by_id():
  a=client.service.GetLibraryById('10000000-0000-0000-0000-000000000006')
  m1=re.search(r'\(Library\)\{\s+_caption\s=\s\"',str(a),re.DOTALL)
  if m1:
    return 'true'

def test_get_library_by_id():
  assert get_library_by_id() == 'true'
