import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_guidanceitems_in_view():
  a=client.service.GetGuidanceItemsInView('52d2d5f4-170a-4b25-bc92-0e53fd8c11a1')
  t1=str(a[0][0])

  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d]*.*Metadata_Hash\s=\s[-\d]*.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',t1,re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_get_guidanceitems_in_view():
  assert get_guidanceitems_in_view() == 'true'
