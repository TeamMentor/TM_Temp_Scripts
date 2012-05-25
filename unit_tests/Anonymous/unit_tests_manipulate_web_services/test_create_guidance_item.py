import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def create_guidance_item():
  guidanceitem= client.factory.create('GuidanceItem_V3')
  guidanceitem.libraryId='00000000-0000-0000-0000-000000000050'
  guidanceitem.guidanceType='fbb1db92-c314-4fb0-a0db-1ff82bc2d68f'
  guidanceitem.creatorId='fbb1db92-c314-4fb0-a0db-1ff82bc2d68f'
  guidanceitem.title='googoo'
  guidanceitem.guidanceItemId='00000000-0000-0000-0000-000000000000'
  guidanceitem.guidanceItemId_Original='00000000-0000-0000-0000-000000000000'
  guidanceitem.source_guidanceItemId='00000000-0000-0000-0000-000000000000'
  guidanceitem.delete='false'

  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.CreateGuidanceItem(guidanceitem)
    print guidanceitem
    m1=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',str(a))
    if m1:
      client.service.Logout()
      return 'true'

def test_create_guidance_item():
  assert create_guidance_item() == 'true'
