import suds
import re

stored_responses={}

#Individual web service method calls. They all start with wsmethod. Nice clean code :)
def wsmethod_rbac_has_role(key,client):
  resp=client.service.RBAC_HasRole('ReadArticles')
  stored_responses['RBAC_HasRole:'+key]=resp

def wsmethod_rbac_current_identity_auth(key,client):
  resp=client.service.RBAC_CurrentIdentity_IsAuthenticated()
  stored_responses['RBAC_CurrentIdentity_IsAuthenticated:'+key]=resp

#Invoke every web service method for every single user
def invoke_methods(client,users,methods):
  for key in users.keys():
    if str(key) != 'anonymous':
      guid=client.service.Login(key,users[key])
      match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',guid)
      if match:
        user_properties=client.service.Current_User()
        client.set_options(headers={'CSRF_Token': user_properties['CSRF_Token']})
        call_all_webservice_methods(key,client)
        client.service.Logout()
    else:
        key='anonymous'
        call_all_webservice_methods(key,client)

  #Each method invoked writes its return values to this Hash. The filled hash is returned to the analysis module once all the methods are invoked.
  return stored_responses

#Wrapper to call each and every web service method
def call_all_webservice_methods(key,client):
  wsmethod_rbac_has_role(key,client)
  wsmethod_rbac_current_identity_auth(key,client)
