
import urllib
import json

url = "https://proxy.hxlstandard.org/data.json?filter02=replace-map&clean-whitespace-tags01=service%2Btype&replace-map-url02=https%3A//docs.google.com/spreadsheets/d/1J_f0bnJEfE87d13_brOyvLjKw4q1xMmHNAHzJc_kmpA/pub%3Fgid%3D0%26single%3Dtrue%26output%3Dcsv&filter01=clean&strip-headers=on&url=https%3A//docs.google.com/spreadsheets/d/1C9fmpzb3VhoGOsCnRAnhbXZNkKd3sVZIN0Ha1VOBQjk/export%3Fformat%3Dcsv%26id%3D1C9fmpzb3VhoGOsCnRAnhbXZNkKd3sVZIN0Ha1VOBQjk%26gid%3D1142452757"

### Read in data

response = urllib.urlopen(url)
data = json.loads(response.read())



# Extract  data column names
column_names = []
count = 0
for i in data[0]:
	count += 1
	x = i.split("+")
	if len(x) > 1:
		column_names.append(str("-".join(x[1:])))
	else:
		column_names.append("x" + str(count))


# Rename for convenience

column_names[5] = "type_org"
column_names[7] = "type_focus"
column_names[8] = "name_country"
column_names[10] = "name_region"



# our categories
cats = ["title","data","language","type_focus","country","region","latitude","longitude","address","landline","mobile","url"]

def isEmpty(val):
	return any([val == "" , val.lower() == "no data" , val.rstrip().lstrip() == "-"])

def convertEmpty(val):
	if isEmpty(val):
		return ""
	else:
		return val

def handleTitle(obj):
	return	" -- ".join(filter(None, [convertEmpty(obj["name"]),convertEmpty(obj["name-en"])]))

def handleData(obj):
	return	" -- ".join(filter(None, [convertEmpty(obj["type_org"]),convertEmpty(obj["description"])]))

# language of service. Current info however is in English!
def handleLang(obj):
	return convertEmtpy(obj["language"])

def handleFocus(obj):
	return convertEmtpy(obj["type_focus"])

def handleCountry(obj):
	return convertEmtpy(obj["name_country"])

def handleRegion(obj):
	return convertEmtpy(obj["name_region"])

def handleAddress(obj):
	return convertEmtpy(obj["address"])

def handleURL(obj):
	return convertEmtpy(obj["url"])

def handleOther(obj):
	tmp = filter(None, [convertEmpty(obj["url-twitter"]),convertEmpty(obj["url-fb"]), convertEmpty(obj["url-instagram"])])
	if len(tmp) > 0:
		return "\n".join(tmp)
	else:
		return ""

def obtainCoordinates(obj):
	address = convertEmtpy(obj["address"])
	if not isEmpty(address):
		gurl = "http://maps.google.com/maps/api/geocode/json?address="
		gurl += (obj["address"],"utf-8" + " " + obj["name_region"] + " " + obj["name_country"]).encode("utf-8")
		gresponse = urllib.urlopen(gurl)
		gloc = response.read()
		f = urllib.urlopen(gurl)
		gdata = f.read()
		lat = json.loads(gdata)["results"][0]["geometry"]["location"]["lat"]
		lon = json.loads(gdata)["results"][0]["geometry"]["location"]["lng"]
		return [lat,lon]
	else:
		return ["",""]

def convertFocus(val,mapping):
	focus_areas = val.split(",")
	renamed_focus = []
	for ff in focus_areas:
		tmp = ff.rstrip().lstrip()
		if not tmp in mapping:
			print("\n\n************* Error with Focus Area Keys *************** " + tmp + " \n\n")
		else:
			renamed_focus.append(mapping[tmp])
	# return list(set([item for sublist in renamed_focus for item in sublist]))
	return renamed_focus

# Re-arrange data to match our format

output = []
all_focus = []
for tt in data[1:]:
	tmp_obj = dict(zip(column_names, tt))
	tmp_out = dict();
	tmp_out["title"] = handleTitle(tmp_obj)
	tmp_out["data"] = handleData(tmp_obj)
	tmp_out["language"] =  "English" #handleLang(tmp_obj)
	# tmp_out["type_focus"] = handleFocus(tmp_obj)
	tmp_out["type_focus"] = convertFocus(convertEmpty(tmp_obj["type_focus"]),focus_mapping)
	all_focus.append(handleFocus(tmp_obj).split(","))
	tmp_out["country"] = handleCountry(tmp_obj)
	tmp_out["region"] = handleRegion(tmp_obj)
	tmp_out["address"] = handleAddress(tmp_obj)
	# obtaiing coordinates is unreliable due to inconsistencies and typos in the data
	# tmp_address = obtainCoordinates(tmp_obj)
	# tmp_out["latitude"] = tmp_address[0]
	# tmp_out["longitude"] = tmp_address[1]
	tmp_out["latitude"] = ""
	tmp_out["longitude"] = ""
	tmp_out["landline"] = ""
	tmp_out["mobile"] = ""
	tmp_out["url"] = handleURL(tmp_obj)
	tmp_out["other"] = handleOther(tmp_obj)
	output.append(tmp_out)



with open('../whoWhatWhere.json', 'w') as outfile:
    json.dump(output, outfile)




########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
### Convergin focus areas
########################################################################################

# carried this out after running loop above once. Then went back and re-ran for-loop with 
# new knowledge from here.

focus_areas = set([item for sublist in all_focus for item in sublist])

#set([u'Information', u' Aid Distribution', u' Camp Management', '', u' Shelter', u'WASH', u'Other', 
#u'Health', u' Emergency Telecommunications', u'Shelter', u' WASH', u'Logistics', u' Logistics', 
#u'Legal Support', u'Cash', u' Education', u'Aid Distribution', u'Camp Management', u' Legal Support', 
#u' Information', u' Other', u' Health', u'Emergency Telecommunications', u'Education', u'Coordination'])

focus_mapping = dict()
focus_mapping["Information"] = "General Information"
focus_mapping["Aid Distribution"] = "General Aid"
focus_mapping["Camp Management"] = "Shelter"
focus_mapping["Shelter"] = "Shelter"
focus_mapping["WASH"] = ["Shelter","Health/Medical"]
focus_mapping["Other"] = "General Aid"
focus_mapping["Health"] = "Health/Medical"
focus_mapping["Emergency Telecommunications"] = "Emergency Responders"
focus_mapping["Logistics"] = "General Information"
focus_mapping["Legal Support"] = "Legal Support"
focus_mapping["Cash"] = "Money/Finances"
focus_mapping["Education"] = "Education"
focus_mapping["Coordination"] = "General Information"
focus_mapping[""] = ""

# our "type_focus"
focus = ["Health/Medical", "Transportation", "Money/Finances", "Shelter", "Clothing", "Food", "Markets", 
"Safety/Security", "Jobs", "Registration Information", "NGO, Charitable Organization, Places of Worship",
 "Government Organisation", "Emergency Responders", "Power—Recharge phone", "Education",
"Family services", "General Information"]

