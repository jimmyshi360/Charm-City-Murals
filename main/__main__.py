import preprocess
import os
import sys
from random import random
from flask import Flask, request, render_template, jsonify
import base64

# Local imports. We'd resolve this is we had time to refactor
sys.path.append('/home/bltar/HopHacksDreamTeam/')


app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.route("/discover")
def canvas():
    return render_template("canvas.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/")
def index():
    return render_template("index.html")

# Out API
@app.route("/api", methods=["POST"])
def api():
    meta = {"has_mural": False}
    return jsonify(meta)

if (__name__ == '__main__'):
# Bind to PORT if defined, otherwise default to 80.
    port = process.env.PORT||'8000';
    app.run(host='0.0.0.0', port=port)
