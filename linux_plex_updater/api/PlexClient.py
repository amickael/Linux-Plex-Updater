import uuid
import logging

import requests


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
        # Try to fetch auth token
        req = requests.post(
            "https://plex.tv/users/sign_in.json",
            params={"X-Plex-Client-Identifier": str(self.identifier)},
            auth=(self.username, self.password),
        )

        # If request is successful set auth token
        if req.ok:
            response = req.json()
            return response.get("user", {}).get("authToken")
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
