import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_guidanceitems_in_folder():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  a=client.service.GetGuidanceItemsInFolder('3fcccd99-3e67-47ec-89f3-d679d6e66fd3')
  t1=str(a[0][0])

  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d]*.*Metadata_Hash\s=\s[-\d]*.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',t1,re.DOTALL)
  if match:
    return 'true'
    #client.service.Logout()

def test_get_guidanceitems_in_folder():
  assert get_guidanceitems_in_folder() == 'true'
