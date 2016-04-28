
import urllib2
from bs4 import BeautifulSoup

def readUrlContent(url):
	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content)
	return soup

def checkLink(url):
	suburl = url.split("/")[-1]
	return "List_of_cities" in suburl and "&" not in suburl and ":" not in suburl and "Europe" not in suburl

## List of countries

url = "https://en.wikipedia.org/wiki/Lists_of_cities_in_Europe"

soup = readUrlContent(url)

list_elems = soup.findAll("li")
for li in list_elems:
	try:
		curr_url = li.find("a", href=True)["href"]
		if checkLink(curr_url):
			print curr_url
			full_url = "https://en.wikipedia.org" + curr_url
			country_soup = readUrlContent(full_url)
			#find all tables and first column with text
	except:
		x = 1



# column_headers = ["City","Region","Municipality","District","Name",
# 	"Metropolitan Area","County","City/Town","Town","Autonomous community"]



