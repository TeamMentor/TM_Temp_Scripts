import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def remove_guidance_items_from_view():
  guid=client.service.Login('editor','4add6f028b8fa65ab9e1057cc2e365321c0812bc1e0a3bf4e3b6bd632ffa4540')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.RemoveGuidanceItemsFromView('d09a1340-a411-4b53-8f24-520dc8d5abb9','00000000-0000-0000-0000-0000008c0633')
    if a:
      client.service.Logout()
      return 'true'

def test_remove_guidance_items_from_view():
  assert remove_guidance_items_from_view() == 'true'
