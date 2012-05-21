import suds
import re

url='http://50.16.28.105:8000/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)

def get_all_folders():

def test_get_all_folders():
  assert get_all_folders() == 'true'
