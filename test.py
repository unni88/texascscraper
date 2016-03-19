from __future__ import print_function
from selenium import webdriver
from lxml import html
import os
import requests

from tinydb import TinyDB, Query

webdriverlocation = "/Users/Unni/Desktop/Drivers/chromedriver"  ###need to change this or find an alternative generic way...
urltomatchforscrape = "http://texassupremecourt.mediasite.com/mediasite/FileServer/Presentation/"
searchurl = "http://www.texasbarcle.com/CLE/TSCSearchResults.asp"


class CaseInfo:
    def __init__(self, caseid, casename, videourl, isbrokenurl):
        self.caseid = caseid
        self.casename = casename
        self.videourl = videourl
        self.isbrokenurl = isbrokenurl



def getvideosourceinfo(urltoscrape):
	driver = webdriver.Chrome(executable_path = webdriverlocation)
	try:
		driver.get(urltoscrape)
		script_tags  = driver.find_elements_by_tag_name('script')
		videoinfosource  = ""
		for script_tag in script_tags:
			scriptsrc =  script_tag.get_attribute('src')
			if urltomatchforscrape in scriptsrc:
				videoinfosource = scriptsrc
		videoinfosource = videoinfosource.split("?",1)[0]
		finalvideosource = getactualvideolink(videoinfosource)
	except Exception,e:
			finalvideosource = False
	driver.close()
	return finalvideosource


def getactualvideolink(videoinfourl):
	finalSource  = ""
	page = requests.get(videoinfourl)
	semicolonlines  = page.content.split(";")
	for semicolonline in semicolonlines:
		if '=' in semicolonline and 'MimeType:"video/mp4' in semicolonline:
			params = semicolonline.split(",")
			for param in params:
				if("Location:" in param):
					finalSource = param.split("Location:",1)[1]
	return finalSource


def getAllSearchResults():
    cases = []
    page = requests.get(searchurl)
    htmltree = html.fromstring(page.content)
    urls = htmltree.xpath('//a[contains(@title,("View video of this presentation"))]')
    ### anchor tag with the title  View video  href
    for index, url in enumerate(urls):
        videosource = searchurl.split("TSCSearchResults.asp")[0] + "" + url.attrib['href']
        casenamewithid = url.text.split("- view video")[0]
        caseid = casenamewithid[casenamewithid.find("(") + 1:casenamewithid.find(")")]
        caseObject = CaseInfo(caseid, casenamewithid, videosource, False)
        cases.append(caseObject)
    return cases


def prelimsearchURLs():
    db = TinyDB('db.json')
    prelimtable = db.table('prelimcasedetails')
    cases = getAllSearchResults()
    prelimtable.purge()
    for idx, case in enumerate(cases):
        prelimtable.insert({'caseid': case.caseid, 'casename': case.casename, 'prelimvideourl': case.videourl,'detailedVideoURL':'0'})

def getdetailedSearchURL():
    db = TinyDB('db.json')
    prelimtable = db.table('prelimcasedetails')
    query = Query()
    elementstoupdate = prelimtable.search(query.detailedVideoURL == '0')
    for iter,element in enumerate(elementstoupdate):
        prelimURL = element['prelimvideourl']
        detailedVideoURL = getvideosourceinfo(prelimURL)
        caseid = element['caseid']
        prelimtable.update({'detailedVideoURL':detailedVideoURL},Query()['caseid'] == caseid)
        # if iter > 1:
        #     break

def main():
    prelimsearchURLs()
    getdetailedSearchURL()



main()
