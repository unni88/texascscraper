from __future__ import print_function 
from selenium import webdriver
from lxml import html
import os
import requests
import random
import time

webdriverlocation = "/Users/Unni/Downloads/chromedriver" ###need to change this or find an alternative generic way...
urltomatchforscrape = "http://texassupremecourt.mediasite.com/mediasite/FileServer/Presentation/"
searchurl = "http://www.texasbarcle.com/CLE/TSCSearchResults.asp"


class CaseInfo:
	def __init__(self,caseid,casename,videourl,isbrokenurl):
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
			print(e)
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
	for index,url in enumerate(urls):
		videosource =  searchurl.split("TSCSearchResults.asp")[0]+""+url.attrib['href']
		casenamewithid =  url.text.split("- view video")[0]
		caseid = casenamewithid[casenamewithid.find("(")+1:casenamewithid.find(")")]
		caseObject = CaseInfo(caseid,casenamewithid,videosource,False)
		cases.append(caseObject)
	return cases	


def main():
   	"""
   	cases = getAllSearchResults()
   	for idx, case in enumerate(cases):
		with open('casedetailfiles.txt','a') as casedetsf:
			casedetsf.write((case.caseid+"##"+case.casename+"##"+case.videourl+"##nope\n").encode('utf8'))  	
	"""





	alreadyprocessedcases=[]
	if os.path.isfile('casedetailstatus.txt'):
		with open('casedetailstatus.txt','r') as casedetsstatusread:
			alreadycaseslines = casedetsstatusread.readlines()
			for alreadycasesline in alreadycaseslines:
			 	alreadyprocessedcases.append(alreadycasesline.split("##")[0])




	allreadlines = []		
	with open('casedetailfiles.txt','r+') as casedetsread:
		allreadlines = casedetsread.readlines()
		iteratelines = allreadlines
		for index,line in enumerate(iteratelines):		
			casedetsarr = line.split("##")
			if((len(casedetsarr)>=3)  and not casedetsarr[0] in alreadyprocessedcases):
				flag = getvideosourceinfo(casedetsarr[2])
		   		finalvideourl = casedetsarr[2]	   			
		   		if(flag != False):
		   			finalvideourl = flag
					allreadlines[index] = line.split("##")[0]+"##"+line.split("##")[1]+"##"+finalvideourl+"##done\n"
					with open('casedetailstatus.txt','a') as casedetsmodify:
						casedetsmodify.write((allreadlines[index]))
				else:
					allreadlines[index] = line.split("##")[0]+"##"+line.split("##")[1]+"##"+line.split("##")[2]+"##broken\n"	
				
					
	
	  
main()


