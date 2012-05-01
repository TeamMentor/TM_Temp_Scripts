import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def create_article():
  article = client.factory.create('TeamMentor_Article')
  metadata = client.factory.create('TeamMentor_Article_Metadata')

  article._Metadata_Hash = '12345678'
  metadata.Id = '10001111-0000-0000-0000-11110011'
  metadata.Title='RVP'

  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.CreateArticle(metadata)
    print a

def test_create_article():
  assert create_article() == 'true'
