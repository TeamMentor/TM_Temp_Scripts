import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_guidanceitems_by_id():
  a=client.service.GetGuidanceItemById('16c073b9-e951-4f25-a282-e867d2d808f7')
  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d]*.*Metadata_Hash\s=\s[-\d]*.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',str(a),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'
