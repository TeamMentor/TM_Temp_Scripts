import suds
import re
import sys
import os
import datetime
from lxml import etree

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname(os.path.abspath(__file__))+'/modules'
sys.path.insert(0, cmd_folder)
#Importing custom external modules
import setup
import authorization
import ws_method
import xml_writer

#Enter WSDL Url here
url='http://50.16.28.105:8000//aspx_pages/TM_WebServices.asmx?WSDL'

def main():
  #Connect to website and retrieve object which contains WSDL details
  client=setup.connect(url)

  #Get usernames and password of the users you need to login with from a file. This file needs to be manually filled in with data in a userTABpassword format
  users=setup.get_users_passwords()

  #Get exact list of all methods exported by the Webservice.
  methods=setup.get_methods_parameters_datatypes(client)

  #Who are the attackers for each method? Who can query but are NOT supposed to query each method? Fill up a list of attackers per method. We haven't yet started any querying though
  methods=authorization.map_adversaries_to_methods(methods)

  #Login as each potential adversary and query each method
  stored_responses=ws_method.invoke_methods(client,users,methods)

  #Generate XML from received responses
  xml_responses=xml_writer.generate_xml_response(stored_responses)

  #Analyze XML responses and store analysis in hash
  report=authorization.analysis(xml_responses,methods)

  #Generate final report in XML format from hash
  xml_writer.create_report(report)

#Code starts running here
main()
