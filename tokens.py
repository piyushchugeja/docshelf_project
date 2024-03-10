import requests
import jwt
import streamlit as st

app_client_id = st.secrets["appClientId"]

def exchange_code_for_token(authorization_code):
    global app_client_id
    token_url = "https://docshelf.auth.us-east-1.amazoncognito.com/oauth2/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": app_client_id,
        "code": authorization_code,
        "redirect_uri": st.secrets["redirectUri"]
    }
    response = requests.post(token_url, data=params)

    if response.status_code == 200:
        tokens = response.json()
        id_token = tokens["id_token"]
        user_info = decode_id_token(id_token)
        return user_info
    else:
        print("Error exchanging code for tokens:", response.text)
        return None

def decode_id_token(id_token):
    try:
        decoded = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": False})
        return decoded
    except Exception as e:
        print("Error decoding id token:", e)
        return None