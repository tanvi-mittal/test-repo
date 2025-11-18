import app
import pytest
import responses


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as c:
        yield c


# ---------------------------
# 200 — Valid username
# ---------------------------
@responses.activate
def test_200_valid_username(client):
    username = "octocat"
    responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        json=[
            {
                "id": "1",
                "description": "Test Gist",
                "html_url": "https://gist.github.com/1",
            }
        ],
        status=200,
    )
    rv = client.get(f"/{username}")
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert data[0]["id"] == "1"
    assert data[0]["description"] == "Test Gist"
    assert data[0]["html_url"] == "https://gist.github.com/1"


# ---------------------------
# 400 — Invalid GitHub usernames
# ---------------------------
def test_400_invalid_username(client):
    rv = client.get("/-octocat")
    assert rv.status_code == 400
    assert rv.get_json()["error"] == "Invalid GitHub username"


# ---------------------------
# 404 — User not found
# ---------------------------
@responses.activate
def test_404_user_not_found(client):
    username = "nonexistentuser"
    responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        json={"message": "Not Found"},
        status=404,
    )
    rv = client.get(f"/{username}")
    assert rv.status_code == 404
    assert rv.get_json()["error"] == "User not found"


# ---------------------------
# 429 — Rate limited
# ---------------------------
@responses.activate
def test_429_rate_limited(client):
    username = "octocat"
    responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        json={"message": "API rate limit exceeded"},
        status=403,
    )
    rv = client.get(f"/{username}")
    assert rv.status_code == 429
    assert rv.get_json()["error"] == "Rate limited by GitHub"


# ---------------------------
# 502 — Forbidden (non-rate limit)
# ---------------------------
@responses.activate
def test_502_forbidden_non_rate(client):
    username = "octocat"
    responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        json={"message": "Access denied"},
        status=403,
    )
    rv = client.get(f"/{username}")
    assert rv.status_code == 502
    assert rv.get_json()["error"] == "Bad Gateway"
    assert rv.get_json()["details"] == "Forbidden by upstream"


# ---------------------------
# 502 — Network error
# ---------------------------
@responses.activate
def test_502_network_error(client):
    username = "octocat"

    def raise_conn_error(_):
        raise responses.ConnectionError("connection failed")

    responses.add_callback(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        callback=raise_conn_error,
    )
    rv = client.get(f"/{username}")
    assert rv.status_code == 502
    assert "connection failed" in rv.get_json()["details"]


# ---------------------------
# 500 — Internal server error
# ---------------------------
@responses.activate
def test_500_internal_error(client, monkeypatch):
    responses.add(
        responses.GET,
        "https://api.github.com/users/octocat/gists",
        json=[{"id": "1", "description": "d", "html_url": "u"}],
        status=200,
    )

    def boom(_):
        raise RuntimeError("boom")

    monkeypatch.setattr(app, "simplify", boom)
    rv = client.get("/octocat")
    assert rv.status_code == 500
    assert rv.get_json()["error"] == "Internal Server Error"


# ---------------------------
# ❌ 404 — Unknown route
# ---------------------------
def test_404_unknown_route(client):
    rv = client.get("/no-such-route")
    assert rv.status_code == 404
    assert rv.get_json()["error"] == "User not found"
