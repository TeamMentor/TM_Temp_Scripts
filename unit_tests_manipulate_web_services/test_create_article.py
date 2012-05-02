import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def create_article():
  article = client.factory.create('TeamMentor_Article')
  article.Metadata.Title='Wenger'
  article.Metadata.Library_Id='c6e149df-91c0-43b4-b7ed-bee6a64e1ae1'
  article.Metadata.Id='00000000-0000-0000-0000-000000000002'

  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    a=client.service.CreateArticle(article)
    m1=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',str(a))
    if m1:
      return 'true'

def test_create_article():
  assert create_article() == 'true'
