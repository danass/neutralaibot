import os
import sys
import requests
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    pds_url = os.getenv("ATP_PDS_HOST", "https://bsky.social")
    handle = os.getenv("ATP_AUTH_HANDLE")
    password = os.getenv("ATP_AUTH_PASSWORD")

    if not handle or not password:
        print("Error: Missing credentials. Set ATP_AUTH_HANDLE and ATP_AUTH_PASSWORD in your .env file.")
        sys.exit(1)

    return pds_url, handle, password

def login(pds_url, handle, password):
    try:
        response = requests.post(
            f"{pds_url}/xrpc/com.atproto.server.createSession",
            json={"identifier": handle, "password": password},
            timeout=10
        )
        response.raise_for_status()
        print("Login successful.")
        return response.json()
    except requests.RequestException as error:
        print(f"Login failed: {error}")
        sys.exit(1)