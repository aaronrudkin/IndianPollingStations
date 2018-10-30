""" Scrapes psleci.nic.in using Mechanize into a triple of state-district-AC values. """

# pylint: disable=unsubscriptable-object
import json  # To save results
import time  # Time lets us rest between lookups
import mechanize  # Mechanize fakes a full browser


def scrape():
	""" Main scraper. """

	# First we are going to look up all the states
	print "Opening first stage lookup..."

	# Create a new browser
	scrape_browser = mechanize.Browser()

	# Some basic settings that might help
	scrape_browser.set_handle_robots(False)  # Ignore robots.txt
	scrape_browser.set_handle_refresh(True)  # Handle unexpected redirects
	scrape_browser.open("http://psleci.nic.in/Default.aspx")  # Open the page
	scrape_browser.select_form(nr=0)  # On the page, select the first input form

	# The states are the dropdown ddlState, but the first item is "Select" text
	first_level_items = scrape_browser.possible_items("ddlState")[1:]

	# Now we have the states
	print "States: ", first_level_items

	# Okay, now let's get the districts
	second_level_items = {}
	# Loop across each state
	for item in first_level_items:
		print "Doing lookup for state ", item
		# For each state make a new browser (this is to prevent the timeout)
		scrape_browser = mechanize.Browser()

		# Open the main page
		scrape_browser.open("http://psleci.nic.in/Default.aspx")

		# Select the state and press submit
		scrape_browser.select_form(nr=0)
		scrape_browser["ddlState"] = [item]
		scrape_browser.submit()

		# Okay, now the new page should have the districts
		# Select the district and press submit
		scrape_browser.select_form(nr=0)
		second_level_temp = scrape_browser.possible_items("ddlDistrict")[1:]

		# Store districts as a list that is the value associated
		# with the key for the state
		second_level_items[item] = second_level_temp

	# Now we have state-district pairs
	print "State-district pairs:"
	print second_level_items

	# Now let's get state-district-AC triples
	third_level_items = {}

	# Loop over each set of dict key-value pairs
	for key, value in second_level_items.iteritems():
		# We're now going to make this a list inside
		# a dict inside a dict:
		# {"State": {"District1": [AC, AC, AC], "District2": [AC, AC, AC], ...}, ...}
		# First, we pre-allocate the second level dict
		if key not in third_level_items:
			third_level_items[key] = {}

		# Now we loop through each district in the districts list
		# for this state
		for v in value:
			# Okay, so key is the state, v is the district
			print "Doing looking for state-district ", key, v

			# New browser
			scrape_browser = mechanize.Browser()

			# Open new page
			scrape_browser.open("http://psleci.nic.in/Default.aspx")

			# Select form, select state, and submit
			scrape_browser.select_form(nr=0)
			scrape_browser["ddlState"] = [key]
			scrape_browser.submit()

			# Select form, select district, and sumbit
			scrape_browser.select_form(nr=0)
			scrape_browser["ddlDistrict"] = [v]
			scrape_browser.submit()
			scrape_browser.select_form(nr=0)

			# Now we get all the AC values
			third_level_temp = scrape_browser.possible_items("ddlAC")[1:]
			third_level_items[key][v] = third_level_temp

		time.sleep(2)

	print "State-district-AC triples:"
	print third_level_items

	# Save the results
	with open("triples.json", "w") as f:
		f.write(json.dumps(third_level_items))

if __name__ == "__main__":
	scrape()
