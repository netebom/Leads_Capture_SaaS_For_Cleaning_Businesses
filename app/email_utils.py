def send_new_lead_email(to_email, lead):
    """
    Email sending is disabled for MVP stability.
    Lead capture must NEVER fail because of email.
    """
    print("New lead captured (email disabled):")
    print(f"To: {to_email}")
    print(lead)
