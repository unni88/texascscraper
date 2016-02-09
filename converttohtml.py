	
def writesourcestohtml():
	f = open('scctexas.html','w')
	htmltexttowrite = "<html><head></head><body><table style='border: 2px solid #CCC;width:100%'>"	
   	htmltexttowrite = htmltexttowrite+"<tr><th style='width:10%'>Row</th><th style='width:10%'>Case No</th><th style='width:40%'>Case Name</th><th style='width:40%'>Video URL</th></tr>"
	index = 1
	with open('casedetailstatus.txt','r') as casedetsreadlines:	
		for caseinfoline in casedetsreadlines:		
			ci = caseinfoline.split("##")
		  	if((len(ci) >= 4)  and  ("done" in ci[3])):					   			
					htmltexttowrite = htmltexttowrite + "<tr><td style='border: 2px solid #CCC;'>"+str(index)+"</td><td style='border: 2px solid #CCC;'>"+ci[0]+"</td><td style='border: 2px solid #CCC;'>"+ci[1]+'</td><td style="border: 2px solid #CCC;"><a href="'+ci[2][1:-1]+'" title="See Video">'+"See Video"+"</a></td></tr>"
					index = index + 1
	htmltexttowrite = htmltexttowrite + "</table></body></html>"
	f.write(htmltexttowrite) 


writesourcestohtml()	