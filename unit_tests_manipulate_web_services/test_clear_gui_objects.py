import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def clear_gui_objects():
  a=client.service.ClearGUIObjects()
  if str(a) == 'True':
    return 'true'

def test_clear_gui_objects():
  assert clear_gui_objects() == 'true'
