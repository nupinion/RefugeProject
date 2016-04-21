
import urllib
import json

url = "https://proxy.hxlstandard.org/data.json?filter02=replace-map&clean-whitespace-tags01=service%2Btype&replace-map-url02=https%3A//docs.google.com/spreadsheets/d/1J_f0bnJEfE87d13_brOyvLjKw4q1xMmHNAHzJc_kmpA/pub%3Fgid%3D0%26single%3Dtrue%26output%3Dcsv&filter01=clean&strip-headers=on&url=https%3A//docs.google.com/spreadsheets/d/1C9fmpzb3VhoGOsCnRAnhbXZNkKd3sVZIN0Ha1VOBQjk/export%3Fformat%3Dcsv%26id%3D1C9fmpzb3VhoGOsCnRAnhbXZNkKd3sVZIN0Ha1VOBQjk%26gid%3D1142452757"


response = urllib.urlopen(url)
data = json.loads(response.read())


# get data column names
column_names = []
for i in data[0]:
	x = i.split("+")
	if len(x) > 1:
		column_names.append(str("-".join(x[1:])))
	else:
		column_names.append("")


column_names[5] = "type_org"
column_names[7] = "type_focus"
column_names[8] = "name_country"
column_names[10] = "name_region"


# our categories
cats = ["title","data","language","type_focus","country","region","latitude","longitude","address","landline","mobile","url"]

def handleTitle(obj):
	return obj["name"] + ";" + obj["name-en"]

def handleData(obj):
	return obj["type_org"] + ". " + obj["description"]

def handleLang(obj):
	return obj["language"]

def handleFocus(obj):
	return obj["type_focus"]

def handleCountry(obj):
	return obj["name_country"]

def handleRegion(obj):
	return obj["name_region"]

def handleAddress(obj):
	return obj["address"]

def handleURL(obj):
	return obj["url"]

def handleOther(obj):
	return "\n" + obj["url-twitter"] + "\n" + obj["url-fb"] + "\n" + obj["url-instagram"]

def obtainCoordinates(obj):
	address = obj["address"]
	gurl = "http://maps.google.com/maps/api/geocode/json?address="
	gurl += obj["address"] + " " + obj["name_region"] + " " + obj["name_country"]
	gresponse = urllib.urlopen(gg)
	gloc = response.read()
	f = urllib.urlopen(gg)
	gdata = f.read()
	lat = json.loads(gdata)["results"][0]["geometry"]["location"]["lon"]
	lon = json.loads(gdata)["results"][0]["geometry"]["location"]["lng"]
	return [lat,lon]


# our "type_focus"
focus = ["Health/Medical", "Transportation", "Money/Finances", "Shelter", "Clothing", "Food", "Markets", "Safety/Security", "Jobs", "Registration Information", "NGO, Charitable Organization, Places of Worship", "Government Organisation", "Emergency Responders", "Power—Recharge phone", "Education",
"Family services", "General Information"]

