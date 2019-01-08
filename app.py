
# -------------------------------------------------------
# App setup
# -------------------------------------------------------
from flask import Flask, render_template, request, escape
app = Flask(__name__)



# -------------------------------------------------------
# Functions
# -------------------------------------------------------
def log_file_exists(path):
	"""
    Check if the log file exists and can be openend
	"""
	try:
		f = open(path)
		f.close()
	except IOError:
		return False
	return True


def log_request(request, where, forecast):
	"""
	Log the location requests and write them to a log file
	"""
	from time import gmtime, strftime
	current = strftime("%d/%m/%Y %H:%M:%S", gmtime())

	with open('locations.log', 'a') as log:
		#print(request.remote_addr, file=log) # IP address
		#print(request.user_agent, file=log) # User agent
		#print(where.title(), current, forecast, file=log, sep=' | ')
		
		temperature = str(forecast['temperature']) + '&#176;C'
		weather = forecast['weather']
		print(where.title(), current, temperature, weather, file=log, sep=' | ')
		

# -------------------------------------------------------
# Pages
# -------------------------------------------------------
@app.route("/")
def index():
	return render_template("index.html", title="Home", **locals())



@app.route("/weather", methods=["GET", "POST"])
def the_weather():
	from engine import Location

	"""
	The location is coming from the form
	The location is coming from the GET parameter in the URL
	"""
	if request.method == "POST":
		form_data = request.form
		where = Location(form_data["location"])
		forecast = where.get_location_data()
		log_request(request, form_data["location"], forecast)

	else:
		get_data = request.args.get('location', type=str)
		if "geo" == get_data:
			import geocoder
			g = geocoder.ip('me')
			if g.ok:
				where = Location('', g.latlng[0], g.latlng[1])
				forecast = where.get_ip_data()

		else:
			where = Location(get_data)
			forecast = where.get_location_data()

	"""
	Render the template. Beware of a 404 return on the forecast.
	"""
	if forecast != 404:
		return render_template("weather.html", title="Weather", **locals())

	else:
		wrong_location = form_data["location"]
		return render_template("change.html", title="Change location", **locals())
	

@app.route("/change")
def change():
    return render_template("change.html", title="Change location", **locals())


@app.route("/viewlog")
def view_log():
	"""
	The import html is needed to unescape the HTML character for degrees.
	"""
	import html
	contents = []
	
	if log_file_exists('locations.log') :
	
		with open('locations.log') as log:
			#contents = log.read()
			for line in log:
				contents.append([])
				for item in line.split('|'):
					contents[-1].append(html.unescape(item))
	
	return render_template("viewlog.html", title="Logs", contents=contents)
	

@app.route("/about")
def about():
    return render_template("about.html", title="About", **locals())




# -------------------------------------------------------
# The execution
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)