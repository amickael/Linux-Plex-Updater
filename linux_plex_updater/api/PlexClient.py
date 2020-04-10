import os
import uuid
import logging

import requests

import linux_plex_updater


class PlexClient:
    def __init__(
        self, username: str, password: str, host: str, port: int,
    ):
        self.identifier = uuid.uuid4()
        self.username = username
        self.password = password
        self.auth_token = self.login()
        self.location = f"{host}:{port}"

    def login(self) -> str:
        # Try to load from cache
        cache_file = os.path.join(
            os.path.dirname(os.path.abspath(linux_plex_updater.__file__)), ".cache"
        )

        # Check if cached token is still valid
        if os.path.isfile(cache_file):
            with open(cache_file, "r") as f:
                auth_token = f.read().strip()
            req = requests.get(
                f"{self.location}/system", params={"X-Plex-Token": auth_token}
            )
            if req.ok:
                return auth_token

        # Try to fetch auth token
        req = requests.post(
            "https://plex.tv/users/sign_in.json",
            params={
                "X-Plex-Client-Identifier": str(self.identifier),
                "X-Plex-Device-Name": "Plex auto-updater",
            },
            auth=(self.username, self.password),
        )

        # If request is successful set auth token and cache for later
        if req.ok:
            auth_token = req.json().get("user", {}).get("authToken")
            with open(cache_file, "w") as f:
                f.write(auth_token)
            return auth_token
        # Otherwise display an error message
        else:
            status_codes = {401: "Invalid username or password"}
            logging.error(status_codes.get(req.status_code, "Authorization failed"))

    def check_updates(self) -> (str, None):
        # Try to update information, retry once to refresh token if invalid
        retry = 0
        while True:
            req = requests.get(
                f"{self.location}/updater/status",
                headers={"Accept": "application/json"},
                params={"X-Plex-Token": self.auth_token},
            )
            if req.ok:
                break
            elif retry > 1:
                return None
            else:
                retry += 1
                self.login()

        # Fetch update information, terminate if no download URL
        download_url = req.json().get("MediaContainer", {}).get("downloadURL")
        if not download_url:
            return None

        # Return true URL
        req = requests.head(download_url, allow_redirects=True,)
        return req.url
