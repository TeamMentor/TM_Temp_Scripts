import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def GetGuidanceItemsInViews():
  guid=client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    views = client.factory.create('ArrayOfGuid')
    views['guid']='d09a1340-a411-4b53-8f24-520dc8d5abb9'
    a=client.service.GetGuidanceItemsInViews(views)
    m1=re.search(r'^\(ArrayOfTeamMentor_Article\)\{\s+TeamMentor_Article\[\]\s\=\s+\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d]*.*Metadata_Hash\s=\s[-\d]*.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',str(a),re.DOTALL)
    if m1:
      client.service.Logout()
      return 'true'

def test_GetGuidanceItemsInViews():
  assert GetGuidanceItemsInViews() == 'true'
