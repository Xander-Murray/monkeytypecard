from unittest.mock import patch, MagicMock

import requests.exceptions

MOCK_PROFILE = {
    "data": {
        "name": "testuser",
        "personalBests": {
            "time": {
                "15": [{"wpm": 120, "acc": 97, "language": "english"}],
                "30": [{"wpm": 115, "acc": 96, "language": "english"}],
            },
            "words": {
                "10": [{"wpm": 130, "acc": 98, "language": "english"}],
                "50": [{"wpm": 125, "acc": 95, "language": "english"}],
            },
        },
        "typingStats": {"timeTyping": 3661},
    }
}


class TestIndex:
    def test_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.content_type


class TestApiThemes:
    def test_returns_json_with_187_entries(self, client):
        resp = client.get("/api/themes")
        assert resp.status_code == 200
        assert resp.content_type.startswith("application/json")
        data = resp.get_json()
        assert len(data) == 187
        assert all("name" in t for t in data)


class TestMonkeytypeSvgValid:
    @patch("services.monkeytype.get_profile", return_value=MOCK_PROFILE)
    def test_valid_request(self, mock_gp, client):
        resp = client.get("/monkeytype.svg?username=testuser")
        assert resp.status_code == 200
        assert "image/svg+xml" in resp.content_type


class TestMonkeytypeSvgInvalidParams:
    def test_invalid_username(self, client):
        resp = client.get("/monkeytype.svg?username=!!!")
        assert resp.status_code == 400
        assert "image/svg+xml" in resp.content_type

    def test_invalid_time_value(self, client):
        resp = client.get("/monkeytype.svg?username=test&timeValue=999")
        assert resp.status_code == 400
        assert "image/svg+xml" in resp.content_type

    def test_invalid_word_value(self, client):
        resp = client.get("/monkeytype.svg?username=test&wordValue=999")
        assert resp.status_code == 400
        assert "image/svg+xml" in resp.content_type


class TestMonkeytypeSvgApiErrors:
    @patch("services.monkeytype.get_profile")
    def test_api_404(self, mock_gp, client):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_gp.side_effect = requests.exceptions.HTTPError(response=mock_resp)
        resp = client.get("/monkeytype.svg?username=testuser")
        assert resp.status_code == 404
        assert "image/svg+xml" in resp.content_type


class TestMonkeytypeSvgPrivateProfile:
    @patch("services.monkeytype.get_profile")
    def test_private_profile(self, mock_gp, client):
        mock_gp.return_value = {"data": {"personalBests": {}}}
        resp = client.get("/monkeytype.svg?username=testuser")
        assert resp.status_code == 200
        assert "image/svg+xml" in resp.content_type
        assert "private" in resp.data.decode().lower()


class TestRateLimiting:
    @patch("services.monkeytype.get_profile", return_value=MOCK_PROFILE)
    def test_rate_limit_after_30_requests(self, mock_gp, client):
        for i in range(30):
            resp = client.get("/monkeytype.svg?username=testuser")
            assert resp.status_code == 200, f"Request {i+1} should be 200"

        resp = client.get("/monkeytype.svg?username=testuser")
        assert resp.status_code == 429
