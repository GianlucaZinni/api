from flask import redirect, url_for, session, Blueprint, jsonify
from votechain_api.stacks.api import api
from votechain_api.access import verify_actually_register
from votechain_api.stacks.controller.functions.google_auth.index import save_google_user

google_auth = Blueprint("API-GOOGLE_AUTH", __name__)

@google_auth.route("/", methods=["GET", "POST"])
@verify_actually_register
def index():
    """
    Redirect to the Google login page.
    """
    return redirect(url_for("API-GOOGLE_AUTH.google_login"))

# Route to start Google authentication
@google_auth.route("/google/login", methods=["GET", "POST"])
def google_login():
    print(session)
    """
    Initiate Google authentication.
    """
    return api.google_key.authorize(
        callback="http://127.0.0.1:5001/google/login/authorized"
    )

# Route to receive Google's response and authorize the user
@google_auth.route("/google/login/authorized")
def authorized():
    """
    Handle Google's authorization response and save user data.
    """
    response = api.google_key.authorized_response()
    
    if response is None or response.get("access_token") is None:
        return jsonify("Error authorizing with Google"), 401

    # Store the access token in the user's session
    session["google_token"] = response["access_token"]

    user_data = api.google_key.get("userinfo").data
    save_google_user(user_data)

    access_token = response.get('access_token')
    print("REPSONSE", response)
    print("ACCESS TOKEN", access_token)
    return redirect(url_for("API-VOTE_AUTH.register"))

# Route to log out
@google_auth.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Log the user out and clear the session.
    """
    session.clear()
    return redirect(url_for("API-GOOGLE_AUTH.google_login"))