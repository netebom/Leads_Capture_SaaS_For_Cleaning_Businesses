# app/webhooks.py
from app.emailer import send_lead_email

def register_webhooks(event_data):
    print("Webhook received:", event_data)
    send_lead_email(event_data)
