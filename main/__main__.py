import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/discover")
def canvas():
    return render_template("canvas.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/")
def index():
    return render_template("index.html")


if (__name__ == '__main__'):
    # Bind to PORT if defined, otherwise default to 80.
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
