
# -------------------------------------------------------
# App setup
# -------------------------------------------------------
from flask import Flask, render_template, request
app = Flask(__name__)



# -------------------------------------------------------
# Pages
# -------------------------------------------------------

@app.route("/", methods=["POST"])
def index():
    from engine import Location

    form_data = request.form
    if form_data:
        where = Location(form_data["location"])
        forecast = where.get_location_data()
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


@app.route("/about")
def about():
    return render_template("about.html", title="About", **locals())

# -------------------------------------------------------
# The execution
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)