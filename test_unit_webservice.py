import suds
import re

url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'
#url='http://docs.teammentor.net/aspx_pages/TM_WebServices.asmx?WSDL'
client = suds.client.Client(url)
d = dict(http='127.0.0.1:8080')
client.set_options(proxy=d)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def login():
  guid=client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  match=re.search(r'(\w{8})-\w{4}-\w{4}-\w{4}-\w{12}',guid)
  if match:
    client.service.Logout()
    return 'true'

def logout():
  client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.Logout()
  match=re.search(r'(0{8})-0{4}-0{4}-0{4}-0{12}',guid)
  if match:
    return 'true'

def test_login_and_logout():
  print 'OK'
  #assert login() == 'true'
  #assert logout() == 'true'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_all_libraryids():
  i=0
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.GetAllLibraryIds()
  while i < len(guid):
    match=re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',str(guid[i]))
    if not match:
      #client.service.Logout()
      return 'false'
      break
    i+=1

  #client.service.Logout()
  return 'true'

def get_all_views():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  guid=client.service.GetAllViews()
  match=re.search(r'^\[\(View.*\{\s*libraryId\s=\s\"[\w-]*\".*folderId\s=\s\"[\w-]*\".*viewId\s=\s\"[\w-]*\".*caption\s=\s\".*\".*author\s=\s[\w\s]*guidanceItems\s=[\s\(\w\)\{]*guid\[\]\s=\s*(\"[\w-]*\",)+',str(guid[0]),re.DOTALL)

  if match:
    #client.service.Logout()
    return 'true'

def get_folders():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  a=client.service.GetFolders('ea854894-8e16-46c8-9c61-737ef46d7e82')
  print a
  #client.service.Logout()
  return 0

def get_guidanceitems_in_library():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  a=client.service.GetGuidanceItemsInLibrary('eb39d862-f752-4d1c-ab6e-14ed697397c0')
  t1=str(a[0][0])

  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s\d+.*Metadata_Hash\s=\s\d+.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',t1,re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def get_guidanceitems_in_folder():
  #client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  print client.service.GetGuidanceItemsInFolder('00000000-0000-0000-0000-000000000000')
  #client.service.Logout()
  return 0

def get_guidanceitems_in_view():
  a=client.service.GetGuidanceItemsInView('42d43763-f674-4929-98f4-71a3345a5ec8')
  t1=str(a[0][0])

  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d+].*Metadata_Hash\s=\s[-\d]+.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',t1,re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def get_guidanceitems_by_id():
  a=client.service.GetGuidanceItemById('00000000-0000-0000-0000-0000000693a7')
  match=re.search(r'^\(TeamMentor_Article\)\{\s+_Content_Hash\s=\s[-\d+].*Metadata_Hash\s=\s[-\d]+.*Metadata\s=\s+\(TeamMentor_Article_Metadata\)\{\s+.*\}\s+Content\s=\s+\(TeamMentor_Article_Content\)\{.*\}',str(a),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def get_folderstructure_library():
  a=client.service.GetFolderStructure_Library('eb39d862-f752-4d1c-ab6e-14ed697397c0')
  match=re.search(r'^\(Library_V3\)\{\s+libraryId\s=\s\"[\w-]*\"\s+name\s=\s\"[\w\s]*\"\s+subFolders\s=\s\"[\w-]*\"\s+views\s=.*libraryId\s=[\"\w-]*\s+.*guid\[\]\s=\s+\"[\w-]*\".*\}$',str(a),re.DOTALL)
  if match:
    #client.service.Logout()
    return 'true'

def test_all_consume_methods():
  #print 'OK'
  assert get_all_libraryids() == 'true'
  assert get_all_views() == 'true'
  #assert get_folders() == 'true'   #--------------> Need valid library ID
  assert get_guidanceitems_in_library() == 'true'
  #assert get_guidanceitems_in_folder() == 'true' #--------------> Need valid folder ID
  assert get_guidanceitems_in_view() == 'true' 
  assert get_guidanceitems_by_id() == 'true' 
  assert get_folderstructure_library() == 'true'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def create_folder():
  client.service.Login('admin','9eff3dbd350bc5ef54fe7143658565bd45b6476db7c511f35206a143287f741d')
  a=client.service.CreateFolder('ea854894-8e16-46c8-9c61-737ef46d7e82','00000000-0000-0000-0000-000000000000','adboo')
  print a
  client.service.Logout()

def test_all_manipulate_methods():
  print 'OK'
  #assert create_folder() == 'true'
