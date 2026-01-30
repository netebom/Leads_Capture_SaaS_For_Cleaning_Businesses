# app/emailer.py
from app.models import get_setting

def send_lead_email(lead):
    host = get_setting("EMAIL_HOST")
    port = get_setting("EMAIL_PORT")
    print(f"Sending email for lead {lead} via {host}:{port}")
