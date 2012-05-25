import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def update_guidance_item():
  guidanceitem= client.factory.create('TeamMentor_Article')
  guidanceitem.Metadata.Title='Kroenke'
  guidanceitem.Metadata.Library_Id='c6e149df-91c0-43b4-b7ed-bee6a64e1ae1'
  guidanceitem.Metadata.Id='1c43512d-d5ec-4ce9-943f-bacb771316e2'

  guid=client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.UpdateGuidanceItem(guidanceitem)
    if str(a) == 'True':
      client.service.Logout()
      return 'true'

def test_update_guidance_item():
  assert update_guidance_item() == 'true'
