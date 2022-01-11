"""
Macproxy -- A simple HTTP proxy for vintage web browsers
"""

import requests
import argparse
from flask import Flask, request, session, g
from html_utils import transcode_html

app = Flask(__name__)
session = requests.Session()

@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def get(path):
    """
    Builds the request for the HTTP GET method
    """
    url = request.url.replace("https://", "http://", 1)
    headers = {
        "Accept": request.headers.get("Accept"),
        "Accept-Language": request.headers.get("Accept-Language"),
        "Referer": request.headers.get("Referer"),
        "User-Agent": request.headers.get("User-Agent"),
    }
    if app.config["USER_AGENT"]:
        headers["User-Agent"] = app.config["USER_AGENT"]
    resp = session.get(url, params=request.args, headers=headers)
    if "content-type" in resp.headers.keys():
        g.content_type = resp.headers["Content-Type"]
        print("Content-type in response header: " + g.content_type)
    if "location" in resp.headers.keys():
        g.location = resp.headers["Location"].replace("https://", "http://", 1)
        print("Location in response header: " + g.location)
    if resp.headers["Content-Type"].startswith("text/html"):
        return transcode_html(
                resp.content,
                app.config["HTML_FORMATTER"],
                app.config["DISABLE_CHAR_CONVERSION"],
            ), resp.status_code
    return resp.content, resp.status_code

@app.route("/", defaults={"path": ""}, methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
def post(path):
    """
    Builds the request for the HTTP POST method
    """
    url = request.url.replace("https://", "http://", 1)
    headers = {
        "Accept": request.headers.get("Accept"),
        "Accept-Language": request.headers.get("Accept-Language"),
        "Referer": request.headers.get("Referer"),
        "User-Agent": request.headers.get("User-Agent"),
    }
    if app.config["USER_AGENT"]:
        headers["User-Agent"] = app.config["USER_AGENT"]
    resp = session.post(url, data=request.form, headers=headers, allow_redirects=True)
    if "content-type" in resp.headers.keys():
        g.content_type = resp.headers["Content-Type"]
        print("Content-type in response header: " + g.content_type)
    if "location" in resp.headers.keys():
        g.location = resp.headers["Location"].replace("https://", "http://", 1)
        print("Location in response header: " + g.location)
    if resp.headers["Content-Type"].startswith("text/html"):
        return transcode_html(
                resp.content,
                app.config["HTML_FORMATTER"],
                app.config["DISABLE_CHAR_CONVERSION"],
            ), resp.status_code
    return resp.content, resp.status_code

@app.after_request
def apply_caching(resp):
    """
    Modifies the response after the request has been built
    """
    # Workaround for retaining the Content-Type header for f.e. downloading binary files.
    # There may be a more elegant way to do this.
    try:
        resp.headers["Content-Type"] = g.content_type
    except:
        pass
    try:
        resp.headers["Location"] = g.location
    except:
        pass
    return resp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Macproxy command line arguments")
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        action="store",
        help="Port number the web server will run on",
        )
    parser.add_argument(
        "--user-agent",
        type=str,
        default="",
        action="store",
        help="Spoof as a particular web browser, e.g. \"Mozilla/5.0\"",
        )
    parser.add_argument(
        "--html-formatter",
        type=str,
        choices=["minimal", "html", "html5"],
        default="html5",
        action="store",
        help="The BeautifulSoup html formatter that Macproxy will use",
        )
    parser.add_argument(
        "--disable-char-conversion",
        action="store_true",
        help="Disable the conversion of common typographic characters to ASCII",
        )
    arguments = parser.parse_args()
    app.config["USER_AGENT"] = arguments.user_agent
    app.config["HTML_FORMATTER"] = arguments.html_formatter
    app.config["DISABLE_CHAR_CONVERSION"] = arguments.disable_char_conversion
    app.run(host="0.0.0.0", port=arguments.port)
