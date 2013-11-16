from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


@app.route("/")
def index():