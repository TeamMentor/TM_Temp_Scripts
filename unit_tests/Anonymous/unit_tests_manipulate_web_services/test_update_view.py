import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def update_view():
  view= client.factory.create('ns1:View')
  view._id='5b9a4498-b498-42cc-97dd-b4de5c59f5ab'; view._caption='alexsong'
  view._parentFolder=''; view._creatorCaption='arsenal football club'
  view._criteria=''; view._library='10000000-0000-0000-0000-000000000006'

  
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.UpdateView(view)
    if str(a) == 'True':
      client.service.Logout()
      return 'true'

def test_update_view():
  assert update_view() == 'true'
