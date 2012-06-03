import re
import datetime
from lxml import etree

method_correct_value={}; report={}

#Who is allowed to access what?
def map_adversaries_to_methods(methods):
  manual_action_adversary_map={}
  try:
    #Open pre-filled configuration file
    f=open('method_attacker_mapping','rU')
  except:
    print 'Could not open file containing Method & Attacker mapping'

  #Read Method attacker mapping from file and fill up the hash which contained only all methods as keys with potential attackers for each method. This bit is 
  #filling a temp hash up.
  for line in f:
    t1=line.split('\t')
    t1[1]=re.sub(r'\n$',r'',t1[1])
    manual_action_adversary_map[t1[0]]=t1[1]

    #Added expected value code
    t1[2]=re.sub(r'\n$',r'',t1[2])
    method_correct_value[t1[0]]=t1[2]

  #...and now the data from the temp hash is used to fill up the real hash.
  for key in methods.keys():
    t2=key.split('(')
    if t2[0] in manual_action_adversary_map:
      methods[key]=manual_action_adversary_map[t2[0]]

  #...and the filled up hash is returned.
  return methods

#Analyze stored responses
def analysis(xmlresponse,methods):
  map1={}
  for m1 in methods:
    t1=m1.split('(')
    map1[t1[0]]=methods[m1]

  tree = etree.parse(xmlresponse)
  root = tree.getroot()
  for child in root.iterchildren():
    attributes=child.attrib
    t1=attributes['method_user'].split(':')
    if t1[0] in map1:
      t2=map1[t1[0]].split(',')
      if t1[1] not in t2:
        report[t1[0]]=t1[1]

  return report
