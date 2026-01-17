"""Simple Flask app."""

from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello_world():
    """Return a greeting."""
    return "Please subscribe, like, and comment on this video, TY!!!"
