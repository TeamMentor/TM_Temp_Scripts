import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def JsTreeWithFoldersAndGuidanceItems():
  a=client.service.JsTreeWithFoldersAndGuidanceItems()
  match=re.search(r'\(JsTree\)\{\s+data\s=\s+\(ArrayOfJsTreeNode\)\{\s+JsTreeNode\[\]\s=',str(a),re.DOTALL)
  if match:
    return 'true'

def test_JsTreeWithFoldersAndGuidanceItems():
  assert JsTreeWithFoldersAndGuidanceItems() == 'true'
