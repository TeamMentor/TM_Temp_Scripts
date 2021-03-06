import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_guidanceitems_in_library():
  #client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  a=client.service.GetGuidanceItemsInLibrary('4738d445-bc9b-456c-8b35-a35057596c16')
  t1=str(a[0][0])

  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d]*.*Metadata_Hash\s=\s[-\d]*.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',t1,re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_guidanceitems_in_library():
  assert get_guidanceitems_in_library() == 'true'
