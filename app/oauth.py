# app/oauth.py
from app.models import save_page, get_setting

def register_oauth(user_data):
    save_page(user_data)
    print(f"Registered OAuth user: {user_data}")
