import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

def get_guidance_types():
  a=client.service.GetGuidanceTypes()
  print a

def test_get_guidance_types():
  assert get_guidance_types() == 'true'
