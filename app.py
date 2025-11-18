from flask import Flask, jsonify, make_response
import requests
import re

app = Flask(__name__)

USERNAME_RE = re.compile(r"^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$")


# Simplify the gist data to only include relevant fields
def simplify(gists):
    return [
        {
            "id": gist.get("id"),
            "description": gist.get("description") or "No description",
            "html_url": gist.get("html_url"),
        }
        for gist in gists
    ]


# Handle errors from GitHub API responses
def handle_github_error(resp):
    status = resp.status_code

    if status == 404:
        return make_response(jsonify({"error": "User not found"}), 404)

    if status == 403:
        try:
            message = (resp.json().get("message") or "").lower()
        except ValueError:
            message = ""
        if "rate limit" in message:
            return make_response(jsonify({"error": "Rate limited by GitHub"}), 429)
        return make_response(
            jsonify({"error": "Bad Gateway", "details": "Forbidden by upstream"}), 502
        )

    return make_response(
        jsonify({"error": "Bad Gateway", "upstream_status": status}), 502
    )


# Endpoint to get gists for a given GitHub username
@app.route("/<username>", methods=["GET"])
def get_gists(username):
    if not username or not USERNAME_RE.match(username):
        return make_response(jsonify({"error": "Invalid GitHub username"}), 400)
    try:
        resp = requests.get(f"https://api.github.com/users/{username}/gists", timeout=5)

        if not resp.ok:
            return handle_github_error(resp)
        try:
            gists = resp.json()
        except Exception:
            return make_response(
                jsonify(
                    {"error": "Bad Gateway", "details": "Invalid JSON from GitHub"}
                ),
                502,
            )
        try:
            return make_response(jsonify(simplify(gists)), 200)
        except Exception:
            return make_response(jsonify({"error": "Internal Server Error"}), 500)

    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"error": "Bad Gateway", "details": str(e)}), 502)


# Error handler for 404 errors
@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
