# -*- encoding: utf-8 -*-
#
# Access data from hackerspaces.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#

from simplemediawiki import MediaWiki
#Requirement: kitchen

makeinitaly__foundation_api_url = "http://hackerspaces.org/w/api.php"


class Lab(object):
	"""Represents a Lab as it is described on hackerspaces.org."""
	
	def __init__(self):
		self.long = ""
		self.lat = ""
		self.coordinates = ""
		self.province = ""
		self.region = ""
		self.address = ""
		self.city = ""
		self.fablabsio = ""
		self.website = ""
		self.facebook = ""
		self.twitter = ""
		self.email = ""
		self.manager = ""
		self.birthyear = ""
		self.text_it = ""
		self.text_en = ""
		

def get_single_lab(lab_slug, data_format):
	"""Gets data from a single lab from makeinitaly.foundation."""
	wiki = MediaWiki(makeinitaly__foundation_api_url)
	wiki_response = wiki.call({'action': 'query', 'titles':lab_slug, 'prop': 'revisions', 'rvprop': 'content'})
	
	# If we don't know the pageid...
	for i in wiki_response["query"]["pages"]:
		content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]

	print content
	exit()
	# Clean the resulting string/list
	#newstr01 = content.replace("}}", "")
	#newstr02 = newstr01.replace("{{", "")
	#result = newstr02.rstrip("\n|").split("\n|")
	
	# Transform the data into a Lab object
	current_lab = Lab()
	
	result = []
	
	# Add existing data
	for i in result:
		if "coordinates=" in i:
			value = i.replace("coordinates=", "")
			current_lab.coordinates = value
			latlong = []
			if ", " in value:
				latlong = value.rstrip(", ").split(", ")
			elif " , " in value:
				latlong = value.rstrip(" , ").split(" , ")
			else:
				latlong = ["",""]
			current_lab.lat = latlong[0]
			current_lab.long = latlong[1]
		elif "province=" in i:
			value = i.replace("province=", "")
			current_lab.province = value.upper()
		elif "region=" in i:
			value = i.replace("region=", "")
			current_lab.region = value
		elif "address=" in i:
			value = i.replace("address=", "")
			current_lab.address = value
		elif "city=" in i:
			value = i.replace("city=", "")
			current_lab.city = value
		elif "fablabsio=" in i:
			value = i.replace("fablabsio=", "")
			current_lab.fablabsio = value
		elif "website=" in i:
			value = i.replace("website=", "")
			current_lab.website = value
		elif "facebook=" in i:
			value = i.replace("facebook=", "")
			current_lab.facebook = value
		elif "twitter=" in i:
			value = i.replace("twitter=", "")
			current_lab.twitter = value
		elif "email=" in i:
			value = i.replace("email=", "")
			current_lab.email = value
		elif "manager=" in i:
			value = i.replace("manager=", "")
			current_lab.manager = value
		elif "birthyear=" in i:
			value = i.replace("birthyear=", "")
			current_lab.birthyear = value

	if data_format == "dict":
		return current_lab.__dict__
	elif data_format == "object":
		return current_lab
	
	
def get_labs(data_format):
	"""Gets data from all labs from makeinitaly.foundation."""

	wiki = MediaWiki(makeinitaly__foundation_api_url)
	wiki_response = wiki.call({'action': 'query', 'list': 'categorymembers', 'cmtitle': 'Category:Hackerspace','cmlimit': '500'})
	urls = []
	for i in wiki_response["query"]["categorymembers"]:
		urls.append(i["title"].replace(" ", "_"))
	
	labs = {}
	# Load all the Labs
	for i in urls:
		current_lab = get_single_lab(i,data_format)
		labs[i] = current_lab		
	
	return labs

	
def labs_count():
	"""Gets the number of current Labs registered on makeinitaly.foundation."""
	
	labs = get_labs(data_format="dict")
	
	return len(labs)
	

if __name__ == "__main__":
	# Debug
	#a = data_from_makeinitaly_foundation()
	#print a["query"]["categorymembers"]
	b = get_labs(data_format="dict")
	#print b
	#print get_labs(data_format="dict")
	#a = get_fablabs()
	#print a["ouagalab"].name
	#print a["ouagalab"].city
	#b = data_from_fablabs_io()
	#c = fablabs_count()
	#print c
	#print get_fablabs_dict()