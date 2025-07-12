from flask import Flask, request, redirect, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.route("/authorize")
def authorize():
    return redirect(
        f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read_all"
    )

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    token_response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    return jsonify(token_response.json())

@app.route("/activities")
def get_activities():
    access_token = request.args.get("access_token")
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return jsonify(response.json())

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)