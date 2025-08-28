#!/usr/bin/env python3
import sys
import time
import requests
import os
from dotenv import load_dotenv

import jwt

# Load environment variables from .env file
load_dotenv()

# Get PEM file path (command line argument takes precedence over .env)
if len(sys.argv) > 1:
    pem = sys.argv[1]
else:
    pem = os.getenv('GITHUB_APP_PEM_FILE', 'od-oraf-test-app.2025-08-27.private-key.pem')

# Get the Client ID (command line argument takes precedence over .env)
if len(sys.argv) > 2:
    client_id = sys.argv[2]
else:
    client_id = os.getenv('GITHUB_APP_CLIENT_ID', 'Iv23likDpjHD1hbh2mQW')

# Get Installation ID from environment
installation_id = os.getenv('GITHUB_APP_INSTALLATION_ID', '69770355')

# Open PEM
with open(pem, 'rb') as pem_file:
    signing_key = pem_file.read()

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,

    # GitHub App's client ID
    'iss': client_id

}

# Create JWT
encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')

print(f"JWT: {encoded_jwt}")

def get_github_app_token(encoded_jwt):
    """
    Make a GET request to GitHub API to retrieve app information using the JWT.
    
    Args:
        encoded_jwt (str): The encoded JWT token
        
    Returns:
        dict: JSON response from GitHub API or None if request fails
    """
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {encoded_jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()['token']

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


app_token = get_github_app_token(encoded_jwt)
print(f"GitHub App Token: {app_token}")

