from fastkml import  kml
import json

filename = "/Users/denise/Documents/Refugees/greek_police.kml"


doc = file(filename).read()
k = kml.KML()
k.from_string(doc)


features = list(k.features())
f2 = list(features[0].features())
police_info = list(f2[1].features())


# print police_info[0].name
# print police_info[0].description
# print police_info[0].description.split("<br>")
# print police_info[0].ExtendedData


output = []
for ps in police_info:
	tmp = ps.description.split("<br>")
	if len(tmp) != 12:
		print "Error distinguishing values"
		break
	else:
		data = dict()
		for dd in tmp:
			curr = dd.split(":")
			data[curr[0]] = curr[1]
		output.append(data)
		break


################################################################################################
# re-arrange data to match our db

final_data_greek = []
final_data_english = []

for tmp_obj in output:
	tmp_out = dict()
	tmp_out["gr"] = dict()
	tmp_out["en"] = dict()
	# greek info
	tmp_out["gr"]["title"] = "Αστυνομικό Τμήμα".decode("utf-8")
	tmp_out["gr"]["language"] = "ελληνικά".decode("utf-8")
	tmp_out["gr"]["data"] = "αντιμετώπισης καταστάσεων έκτακτης ανάγκης, εγγραφή, γενική βοήθεια.".decode("utf-8")
	tmp_out["gr"]["type_focus"] = ["Safety/Security","Registration Information","Emergency Responders"]
	tmp_out["gr"]["country"] = "Greece"
	tmp_out["gr"]["region"] = "νομός ".decode("utf-8") + tmp_obj["nomos_1"] + ", περιφέρεια ".decode("utf-8") + tmp_obj["perifereia_1"]
	tmp_out["gr"]["address"] = tmp_obj["diefthinsi_forea"]
	tmp_out["gr"]["mobile"] = ""
	tmp_out["gr"]["landline"] = ""
	tmp_out["gr"]["url"] = ""
	tmp_out["gr"]["lat"] = tmp_obj["latitude"]
	tmp_out["gr"]["lon"] = tmp_obj["longitude"]
	final_data_greek.append(tmp_out["gr"])
	# english info
	tmp_out["en"]["title"] = "Police Station"
	tmp_out["en"]["language"] = "English"
	tmp_out["en"]["data"] = "Emergency response, registration, general assistance."
	tmp_out["en"]["type_focus"] = ["Safety/Security","Registration Information","Emergency Responders"]
	tmp_out["en"]["country"] = "Greece"
	tmp_out["en"]["region"] = ""
	tmp_out["en"]["address"] = ""
	tmp_out["en"]["mobile"] = ""
	tmp_out["en"]["landline"] = ""
	tmp_out["en"]["url"] = ""
	tmp_out["en"]["lat"] = tmp_obj["latitude"]
	tmp_out["en"]["lon"] = tmp_obj["longitude"]
	final_data_english.append(tmp_out["en"])


with open('../greek_police_greek.json', 'w') as outfile:
    json.dump(final_data_greek, outfile)

with open('../greek_police_english.json', 'w') as outfile:
    json.dump(final_data_english, outfile)