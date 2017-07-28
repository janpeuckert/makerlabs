# -*- encoding: utf-8 -*-
#
# Access data from hackerspaces.org
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: LGPL v.3
#
#


from classes import Lab

import json
from simplemediawiki import MediaWiki
import mwparserfromhell

hackerspaces_org_api_url = "https://wiki.hackerspaces.org/w/api.php"


class Hackerspace(Lab):

    """Represents a Hackerspace as it is described on hackerspaces.org."""

    def __init__(self):
        self.source = "hackerspaces.org"
        self.lab_type = "Hackerspace"


def get_single_lab(lab_slug):
    """Gets data from a single lab from hackerspaces.org."""
    wiki = MediaWiki(hackerspaces_org_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'titles': lab_slug,
         'prop': 'revisions',
         'rvprop': 'content'})

    # If we don't know the pageid...
    for i in wiki_response["query"]["pages"]:
        content = wiki_response["query"]["pages"][i]["revisions"][0]["*"]

    # Transform the data into a Lab object
    current_lab = Hackerspace()

    equipment_list = []

    # Parse the Mediawiki code
    wikicode = mwparserfromhell.parse(content)
    for k in wikicode.filter_templates():
        element_name = unicode(k.name)
        if "Hackerspace" in element_name:
            for j in k.params:
                if unicode(j.name) == "logo":
                    current_lab.logo = unicode(j.value)
                if unicode(j.name) == "country":
                    current_lab.country = unicode(j.value)
                if unicode(j.name) == "state":
                    current_lab.state = unicode(j.value)
                if unicode(j.name) == "city":
                    current_lab.city = unicode(j.value)
                if unicode(j.name) == "founding":
                    current_lab.city = unicode(j.value)
                if unicode(j.name) == "coordinate":
                    value = unicode(j.value)
                    current_lab.coordinates = value
                    latlong = []
                    if ", " in value:
                        latlong = value.rstrip(", ").split(", ")
                    elif " , " in value:
                        latlong = value.rstrip(" , ").split(" , ")
                    else:
                        latlong = ["", ""]
                    current_lab.latitude = latlong[0]
                    current_lab.longitude = latlong[1]
                if unicode(j.name) == "membercount":
                    current_lab.membercount = unicode(j.value)
                if unicode(j.name) == "fee":
                    current_lab.fee = unicode(j.value)
                if unicode(j.name) == "size":
                    current_lab.size = unicode(j.value)
                if unicode(j.name) == "status":
                    current_lab.status = unicode(j.value)
                if unicode(j.name) == "site":
                    current_lab.site = unicode(j.value)
                if unicode(j.name) == "wiki":
                    current_lab.wiki = unicode(j.value)
                if unicode(j.name) == "irc":
                    current_lab.irc = unicode(j.value)
                if unicode(j.name) == "jabber":
                    current_lab.jabber = unicode(j.value)
                if unicode(j.name) == "phone":
                    current_lab.phone = unicode(j.value)
                if unicode(j.name) == "youtube":
                    current_lab.youtube = unicode(j.value)
                if unicode(j.name) == "eventbrite":
                    current_lab.eventbrite = unicode(j.value)
                if unicode(j.name) == "facebook":
                    current_lab.facebook = unicode(j.value)
                if unicode(j.name) == "ustream":
                    current_lab.ustream = unicode(j.value)
                if unicode(j.name) == "flickr":
                    current_lab.flickr = unicode(j.value)
                if unicode(j.name) == "twitter":
                    current_lab.twitter = unicode(j.value)
                if unicode(j.name) == "googleplus":
                    current_lab.googleplus = unicode(j.value)
                if unicode(j.name) == "email":
                    current_lab.email = unicode(j.value)
                if unicode(j.name) == "maillist":
                    current_lab.maillist = unicode(j.value)
                if unicode(j.name) == "ical":
                    current_lab.ical = unicode(j.value)
                if unicode(j.name) == "forum":
                    current_lab.forum = unicode(j.value)
                if unicode(j.name) == "street-address":
                    current_lab.street_address = unicode(j.value)
                if unicode(j.name) == "postalcode":
                    current_lab.postalcode = unicode(j.value)
                if unicode(j.name) == "region":
                    current_lab.region = unicode(j.value)
                if unicode(j.name) == "post-office-box":
                    current_lab.post_office_box = unicode(j.value)
        elif "Equipment" in element_name:
            for j in k.params:
                equipment_list.append(j.replace("equipment=", ""))

    current_lab.equipment = equipment_list

    # Load the free text
    freetext = ""
    for k in wikicode._nodes:
        try:
            test_value = k.name
        except AttributeError:
            freetext += unicode(k)
    current_lab.text = freetext

    return current_lab


def get_labs(format):
    """Gets data from all labs from hackerspaces.org."""

    labs = []

    # Get the first page of data
    wiki = MediaWiki(hackerspaces_org_api_url)
    wiki_response = wiki.call(
        {'action': 'query',
         'list': 'categorymembers',
         'cmtitle': 'Category:Hackerspace',
         'cmlimit': '500'})
    nextpage = wiki_response["query-continue"]["categorymembers"]["cmcontinue"]

    urls = []
    for i in wiki_response["query"]["categorymembers"]:
        urls.append(i["title"].replace(" ", "_"))

    # Load all the Labs in the first page
    for i in urls:
        current_lab = get_single_lab(i)
        labs.append(current_lab)

    # Load all the Labs from the other pages
    while "query-continue" in wiki_response:
        wiki = MediaWiki(hackerspaces_org_api_url)
        wiki_response = wiki.call({'action': 'query',
                                   'list': 'categorymembers',
                                   'cmtitle': 'Category:Hackerspace',
                                   'cmlimit': '500',
                                   "cmcontinue": nextpage})

        urls = []
        for i in wiki_response["query"]["categorymembers"]:
            urls.append(i["title"].replace(" ", "_"))

        # Load all the Labs
        for i in urls:
            current_lab = get_single_lab(i)
            labs.append(current_lab)

        if "query-continue" in wiki_response:
            nextpage = wiki_response[
                "query-continue"]["categorymembers"]["cmcontinue"]
        else:
            break

    # Transform the list into a dictionary
    labs_dict = {}
    for j, k in enumerate(labs):
        labs_dict[j] = k.__dict__

    # Return a dictiornary / json
    if format.lower() == "dict" or format.lower() == "json":
        output = labs_dict
    # Return a geojson
    elif format.lower() == "geojson" or format.lower() == "geo":
        labs_list = []
        for l in labs_dict:
            single = labs_dict[l].__dict__
            single_lab = Feature(
                type="Feature",
                geometry=Point((single["latitude"], single["longitude"])),
                properties=single)
            labs_list.append(single_lab)
        output = dumps(FeatureCollection(labs_list))
    # Return an object
    elif format.lower() == "object" or format.lower() == "obj":
        output = labs
    # Default: return an object
    else:
        output = labs
    # Return a proper json
    if format.lower() == "json":
        output = json.dumps(labs_dict)
    return output


def labs_count():
    """Gets the number of current Hackerspaces registered on hackerspaces.org."""

    labs = get_labs()

    return len(labs)


if __name__ == "__main__":
    pass
