from flask import Flask, request, jsonify
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# OAuth 2.0 Configuration
# Replace these with your Upstox API credentials and redirect URI
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"


@app.route('/')
def home():
    # Construct the OAuth 2.0 authorization URL
    auth_url = (
        f"https://api.upstox.com/v2/login/authorization/dialog"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=optional_state"
    )
    return f"""
    <h1>Upstox OAuth 2.0 Automation</h1>
    <p>Click the link below to authenticate:</p>
    <a href="{auth_url}" target="_blank">Login with Upstox</a>
    """


@app.route('/callback')
def callback():
    # Capture the `code` and `state` from the redirect URL
    auth_code = request.args.get('code')
    state = request.args.get('state')  # Optional

    if auth_code:
        # Exchange the authorization code for an access token
        payload = {
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(TOKEN_URL, data=payload)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")

            # Fetch portfolio holdings
            url = 'https://api.upstox.com/v2/portfolio/long-term-holdings'
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response_holding = requests.get(url, headers=headers)

            if response_holding.status_code == 200:
                holdings_data = response_holding.json()
                return jsonify({
                    "message": "Access Token successfully retrieved!",
                    "access_token": access_token,
                    #"token_data": token_data,
                    "holdings": holdings_data
                })
            else:
                return f"Failed to fetch holdings: {response_holding.text}", 400
        else:
            return f"Failed to exchange authorization code: {response.text}", 400
    else:
        return "Authorization code not found in the callback request.", 400


if __name__ == '__main__':
    # Run the Flask application
    app.run(port=5000)
