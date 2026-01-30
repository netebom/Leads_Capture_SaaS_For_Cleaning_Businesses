import os
from flask import redirect, url_for
from models import create_demo_page


def register_setup(app):

    @app.route("/setup")
    def setup():
        # DEMO MODE: bypass Facebook completely
        if os.getenv("DEMO_MODE") == "1":
            page = create_demo_page()
            return redirect(f"/dashboard/{page['token']}")

        # Production guard
        if not os.getenv("FACEBOOK_APP_ID"):
            return "Facebook App ID not set. Please complete setup first.", 400

        # Normal OAuth flow would start here
        return "OAuth flow not implemented yet", 501
