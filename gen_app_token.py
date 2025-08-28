#!/usr/bin/env python3
import sys
import time
import requests
import os
from dotenv import load_dotenv

import jwt

# Load environment variables from .env file
load_dotenv()

def generate_jwt_token(pem_file_path=None, client_id=None):
    """
    Generate a JWT token for GitHub App authentication.
    
    Args:
        pem_file_path (str, optional): Path to the PEM private key file
        client_id (str, optional): GitHub App Client ID
        
    Returns:
        str: Encoded JWT token
    """
    # Get PEM file path (parameter takes precedence over command line over .env)
    if pem_file_path:
        pem = pem_file_path
    elif len(sys.argv) > 1:
        pem = sys.argv[1]
    else:
        pem = os.getenv('GITHUB_APP_PEM_FILE', 'od-oraf-test-app.2025-08-27.private-key.pem')

    # Get the Client ID (parameter takes precedence over command line over .env)
    if client_id:
        app_client_id = client_id
    elif len(sys.argv) > 2:
        app_client_id = sys.argv[2]
    else:
        app_client_id = os.getenv('GITHUB_APP_CLIENT_ID', 'Iv23likDpjHD1hbh2mQW')

    # Open PEM
    with open(pem, 'rb') as pem_file:
        signing_key = pem_file.read()

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's client ID
        'iss': app_client_id
    }

    # Create JWT
    encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')
    return encoded_jwt

# Generate JWT token when script is run directly
encoded_jwt = generate_jwt_token()
# print(f"JWT: {encoded_jwt}")

def get_github_app_token(encoded_jwt=None, installation_id=None):
    """
    Make a POST request to GitHub API to create an installation access token using the JWT.
    
    Args:
        encoded_jwt (str, optional): The encoded JWT token. If None, generates a new one.
        installation_id (str, optional): GitHub App Installation ID. If None, uses environment variable.
        
    Returns:
        str: Access token or None if request fails
    """
    # Generate JWT if not provided
    if encoded_jwt is None:
        encoded_jwt = generate_jwt_token()
    
    # Get Installation ID from environment if not provided
    if installation_id is None:
        installation_id = os.getenv('GITHUB_APP_INSTALLATION_ID', '69770355')
    
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


# Generate tokens when script is run directly
if __name__ == "__main__":
    app_token = get_github_app_token(encoded_jwt)
    print(f"GitHub App Token: {app_token}")

