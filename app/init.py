from flask import Flask, render_template

# Initialize Flask app
app = Flask(
    __name__,
    template_folder="templates",  # templates must be in app/templates/
    static_folder="static"        # optional: if you have static files
)

# Import other modules to register routes/functions
from app import webhooks, oauth, dashboard, emailer, models

# Example route to test server
@app.route("/")
def index():
    return render_template("index.html")  # Make sure this file exists
