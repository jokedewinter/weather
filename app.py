
# -------------------------------------------------------
# App setup
# -------------------------------------------------------
from flask import Flask, render_template, request
from engine import *
app = Flask(__name__)


# -------------------------------------------------------
# Pages
# -------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", title="Home", **locals())


@app.route("/weather", methods=["GET", "POST"])
def the_weather():
    """
    The location is coming from the form
    The location is coming from the GET parameter in the URL
    """
    if request.method == "POST":
        form_data = request.form
        where = Location(form_data["location"])
        forecast = where.get_location_data()

        if (forecast == 404) or (len(forecast) < 0):
            wrong_location = form_data["location"]
            return render_template("index.html", title="Change location", **locals())

    else:
        get_data = request.args.get('location', type=str)
        if "geo" == get_data:
            import geocoder
            g = geocoder.ip('me')

            if g.ok:
                where = Location('', g.latlng[0], g.latlng[1])
                forecast = where.get_ip_data()
            else:
                wrong_location = request.remote_addr
                return render_template("index.html", title="Change location", **locals())

        else:
             where = Location(get_data)
             forecast = where.get_location_data()

    """
    Render the template. Beware of a 404 return on the forecast.
    """
    log_request(forecast)
    return render_template("weather.html", title="Weather", **locals())


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

    if log_file_exists('locations.log'):
        for line in reversed(list(open('locations.log'))):
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(html.unescape(item))

        # with open('locations.log') as log:
        #     # contents = log.read()
        #     for line in log:
        #         contents.append([])
        #         for item in line.split('|'):
        #             contents[-1].append(html.unescape(item))

    return render_template("viewlog.html", title="Logs", contents=contents)


@app.route("/about")
def about():
    return render_template("about.html", title="About", **locals())


# -------------------------------------------------------
# The execution
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

