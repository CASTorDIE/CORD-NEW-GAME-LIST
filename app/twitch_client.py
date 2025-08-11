import os
import time
import requests
from typing import Dict, List

TWITCH_OAUTH_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_API = "https://api.twitch.tv/helix"

class TwitchClient:
    def __init__(self):
        self.client_id = os.environ["TWITCH_CLIENT_ID"]
        self.client_secret = os.environ["TWITCH_CLIENT_SECRET"]
        self._token = None
        self._token_expiry = 0

    def _get_app_token(self):
        if self._token and time.time() < self._token_expiry - 60:
            return self._token
        resp = requests.post(TWITCH_OAUTH_URL, data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        })
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 3600)
        return self._token

    def _headers(self) -> Dict[str, str]:
        return {
            "Client-Id": self.client_id,
            "Authorization": f"Bearer {self._get_app_token()}"
        }

    def get_streams(self, after: str = None, first: int = 100) -> Dict:
        params = {"first": min(first, 100)}
        if after:
            params["after"] = after
        r = requests.get(f"{TWITCH_API}/streams", headers=self._headers(), params=params)
        r.raise_for_status()
        return r.json()

    def get_games(self, ids: List[str]) -> Dict:
        # Helix Get Games supports ids[]=...
        params = [("id", gid) for gid in ids]
        r = requests.get(f"{TWITCH_API}/games", headers=self._headers(), params=params)
        r.raise_for_status()
        return r.json()
