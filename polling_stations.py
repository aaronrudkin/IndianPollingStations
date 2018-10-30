""" Takes state-district-AC triple and scrapes all polling stations from psleci.nic.in """

# pylint: disable=unsubscriptable-object,protected-access
import time  # Sleeping
import traceback  # Error handling
import csv  # Write to CSV
import json  # Loading state-district-ac triples from the last script
import requests  # Getting final JSON
import mechanize  # Mechanize fakes a full browser
import bs4  # Getting select labels from forms
import unidecode  # Unicode handling.


def fix_unicode(unicode_list):
	""" Downconverts everything in the row we're writing to ascii. """
	for i in xrange(0, len(unicode_list)):
		if isinstance(unicode_list[i], unicode):
			unicode_list[i] = unidecode.unidecode(unicode_list[i])
	return unicode_list


def get_text_label(value_label, select_name, data):
	""" Given we are selecting item :value_label:, what text is associated with that in :select_name: """
	parser = bs4.BeautifulSoup(data, "html5lib")
	options = parser.find("select", {"name": select_name}).find_all("option")
	text_label = [x.text for x in options if x["value"] == value_label][0]
	return text_label


def read_polling_stations(state, district, ac_number):
	""" Scrape a single state-district-ac triple, returns list of lists """
	rows = []
	result_return = {}

	print "\t\t\t Getting", state, district, ac_number
	browser = mechanize.Browser()
	browser.open("http://psleci.nic.in/Default.aspx")
	browser.select_form(nr=0)
	result_return["state"] = get_text_label(state, "ddlState", browser.response().read())
	browser["ddlState"] = [state]
	browser.submit()
	print "\t\t\t State submitted"
	browser.select_form(nr=0)
	result_return["district"] = get_text_label(district, "ddlDistrict", browser.response().read())
	browser["ddlDistrict"] = [district]
	browser.submit()
	print "\t\t\t District submitted"
	browser.select_form(nr=0)
	result_return["ac_number"] = get_text_label(ac_number, "ddlAC", browser.response().read())
	browser["ddlAC"] = [ac_number]
	browser.submit()
	browser.select_form(nr=0)
	print "\t\t\t AC submitted"
	browser["ddlPS"] = ["ALL"]
	browser.submit()
	print "\t\t\t Asked for polling stations"
	cookiejar = browser._ua_handlers['_cookies'].cookiejar
	for c in cookiejar:
		if c.name == "ASP.NET_SessionId":
			cookies = {c.name: c.value}
			break

	headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
		"Host": "psleci.nic.in",
		"Connection": "keep-alive",
		"Content-Length": "0",
		"Origin": "http://psleci.nic.in",
		"Content-Type": "application/json; charset=UTF-8",
		"Accept": "*/*",
		"DNT": "1",
		"Referer": "http://psleci.nic.in/default.aspx",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US,en;q=0.8,fr;q=0.6"}
	url = "http://psleci.nic.in/GService.asmx/GetGoogleObject"

	print "\t\t\t Getting final JSON"
	r = requests.post(url, headers=headers, cookies=cookies)
	try:
		j = r.json()
		if "d" in j and "Points" in j["d"]:
			for point in j["d"]["Points"]:
				number_name = point["InfoHTML"].split("Polling Station No and Name : ", 1)[1].split("<br/>")[0].strip()
				number, name = [x.strip() for x in number_name.split(" ", 1)]
				web_url = point["InfoHTML"].split("<a href='", 1)[1].split(" ' target", 1)[0].strip()

				rows.append(fix_unicode([result_return["state"], result_return["district"], result_return["ac_number"], point["Latitude"], point["Longitude"], number, name, web_url]))
	except:
		print traceback.format_exc()
		return []
	return rows


def read_all():
	""" Reads all of the state-district-ac triples and scrapes them one by one, outputs list. """
	base_results = [["State", "District", "AC", "Latitude", "Longitude", "PSNumber", "PSName", "WebURL"]]
	with open("out.csv", "ab") as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerows(base_results)

	triples = json.load(open("triples.json", "r"))
	i = 1
	for key, value in triples.iteritems():
		print "Beginning state", i, "/", len(triples)
		state = key
		j = 1
		for dkey, dvalue in value.iteritems():
			print "\t Beginning district", j, "/", len(value)
			district = dkey
			k = 1
			for ackey in dvalue:
				print "\t\t Beginning AC", k, "/", len(dvalue)
				tries = 5
				while tries > 0:
					try:
						ac_results = read_polling_stations(state, district, ackey)
						break
					except:
						time.sleep(3)
						tries = tries - 1

				if tries == 0:
					with open("error.txt", "a") as errorfile:
						errorfile.write("Error in request " + state + ", " + district + ", " + ackey + "\n")

				else:
					with open("out.csv", "ab") as csvfile:
						writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
						writer.writerows(ac_results)

				k = k + 1
				time.sleep(1)  # Short pause between ACs
			j = j + 1
			time.sleep(15)  # Medium pause between districts
		i = i + 1
		time.sleep(30)  # Long pause between states


if __name__ == "__main__":
	open("out.csv", "w")  # Delete the existing results.
	read_all()
