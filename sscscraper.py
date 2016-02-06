from __future__ import print_function 
from selenium import webdriver
from lxml import html
import requests
import random
import time

webdriverlocation = "/Users/Unni/Downloads/chromedriver" ###need to change this or find an alternative generic way...
urltomatchforscrape = "http://texassupremecourt.mediasite.com/mediasite/FileServer/Presentation/"
searchurl = "http://www.texasbarcle.com/CLE/TSCSearchResults.asp"


class CaseInfo:
	def __init__(self,caseid,casename,videourl):
		self.caseid = caseid
		self.casename = casename
		self.videourl = videourl









def getvideosourceinfo(urltoscrape):
	dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (
	     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
	     "(KHTML, like Gecko) Chrome/15.0.87")


	driver = webdriver.Chrome(executable_path = webdriverlocation)
	driver.get(urltoscrape)
	script_tags  = driver.find_elements_by_tag_name('script')
	videoinfosource  = ""
	for script_tag in script_tags:
		scriptsrc =  script_tag.get_attribute('src')
		if urltomatchforscrape in scriptsrc:
			videoinfosource = scriptsrc
	videoinfosource = videoinfosource.split("?",1)[0]		
	finalvideosource = getactualvideolink(videoinfosource)	
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
	for url in urls:
		videosource =  searchurl.split("TSCSearchResults.asp")[0]+""+url.attrib['href']
		casenamewithid =  url.text.split("- view video")[0]
		caseid = casenamewithid[casenamewithid.find("(")+1:casenamewithid.find(")")]
		caseObject = CaseInfo(caseid,casenamewithid,videosource)
		cases.append(caseObject)
	return cases	


def main():
   	cases = getAllSearchResults()
   	f = open('scctexas.html','w')
   	htmltexttowrite = "<html><head></head><body><table style='border: 2px solid #CCC;width:100%'>"
   	for idx, case in enumerate(cases):
	   		seconds = 2 + (random.random() * 2)
			time.sleep(seconds)
	   		case.videourl = getvideosourceinfo(case.videourl)###getvideosourceinfo(chromedriverlocation,case.videourl,urltomatchforscrape)
   	htmltexttowrite = htmltexttowrite+"<tr><th style='width:10%'>Case No</th><th style='width:40%'>Case Name</th><th style='width:40%'>Video URL</th></tr>"
   	for case in cases:
		htmltexttowrite = htmltexttowrite + "<tr><td style='border: 2px solid #CCC;'>"+case.caseid+"</td><td style='border: 2px solid #CCC;'>"+case.casename+'</td><td style="border: 2px solid #CCC;"><a href="'+case.videourl[1:-1]+'" title="See Video">'+case.videourl[1:-1]+"</a></td></tr>"
	###	f.write(case.caseid+":"+case.casename+":"+case.videourl+'\n') # python will convert \n to os.linesep
	htmltexttowrite = htmltexttowrite + "</table></body></html>"
	f.write(htmltexttowrite.encode('utf8'))
main()



###http://www.texasbarcle.com/CLE/TSCPlayVideo.asp?sCaseNo=15-0029