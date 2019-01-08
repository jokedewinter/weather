
# -------------------------------------------------------
# App setup
# -------------------------------------------------------
from flask import Flask, render_template, request, escape
app = Flask(__name__)



# -------------------------------------------------------
# Pages
# -------------------------------------------------------


# Log the location requests and write them to a log file
def log_request(request, where, forecast):
	from time import gmtime, strftime
	current = strftime("%d/%m/%Y %H:%M:%S", gmtime())

	with open('locations.log', 'a') as log:
		#print(request.remote_addr, file=log) # IP address
		#print(request.user_agent, file=log) # User agent
		#print(where.title(), current, forecast, file=log, sep=' | ')
		
		temperature = str(forecast['temperature']) + '&#176;C'
		weather = forecast['weather']
		print(where.title(), current, temperature, weather, file=log, sep=' | ')
		


@app.route("/", methods=["GET", "POST"])
def index():
    from engine import Location

    form_data = request.form
    if form_data:
        where = Location(form_data["location"])
        forecast = where.get_location_data()
        log_request(request, form_data["location"], forecast)
    else:
        import geocoder
        g = geocoder.ip('me')
        if g.ok:
            where = Location('', g.latlng[0], g.latlng[1])
            forecast = where.get_ip_data()

    if forecast != 404:
        return render_template("index.html", title="Home", **locals())
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