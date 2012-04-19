import suds
import re

url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'

def main():
  client=connect_and_login(url)
  get_methods_parameters_datatypes(client)

def connect_and_login(url):
  client = suds.client.Client(url)
  client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match = re.search(r'ASP.NET_SessionId=.*Cookie Session=', str(client.options.transport.cookiejar))
  if match:
    user_properties=client.service.Current_User()
    client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
    return client

def get_methods_parameters_datatypes(client):
  t1=re.findall(r'.*Methods\ \(\d+\)(.*)Types\ \(\d+\)',str(client),re.DOTALL)

main()

#d = dict(http='127.0.0.1:8080')
#client.set_options(proxy=d)
