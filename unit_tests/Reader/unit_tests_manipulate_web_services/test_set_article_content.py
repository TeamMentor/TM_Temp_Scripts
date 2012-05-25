import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def set_article_content():
  guid=client.service.Login('reader','e1c6544c9903f4acbdbe35d97e8f9b6c2abb5e95fa3a4280a49de5a0382cc7ce')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.SetArticleContent('f634adbd-f54d-421f-9d6d-e208b8acbf84','string','abcdefghijklmnopqrstuvwxyz')
    if str(a) == 'True':
      client.service.Logout()
      return 'true'

def test_set_article_content():
  assert set_article_content() == 'true'
