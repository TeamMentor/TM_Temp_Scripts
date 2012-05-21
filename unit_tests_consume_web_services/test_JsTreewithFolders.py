import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsTreeWithFolders():
    a=client.service.JsTreeWithFolders()
    m1=re.search(r'\(JsTree\)\{\s+data\s\=\s+\(ArrayOfJsTreeNode\)\{',str(a),re.DOTALL)
    if m1:
      return 'true'

def test_JsTreeWithFolders():
  assert JsTreeWithFolders() == 'true'
