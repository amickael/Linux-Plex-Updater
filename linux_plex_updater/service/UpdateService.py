import os
import tempfile
import subprocess
import logging
from urllib.parse import urlparse

import requests

from linux_plex_updater.api import PlexClient


class UpdateService:
    def __init__(
        self,
        username: str,
        password: str,
        host: str = "http://localhost",
        port: int = 32400,
    ):
        self.client = PlexClient(username, password, host, port)

    def download_update(self) -> (str, None):
        # Check for outstanding updates
        download_url = self.client.check_updates()
        if not download_url:
            return None

        # Download file into temp dir
        req = requests.get(download_url)
        if req.ok:
            file_path = os.path.join(
                tempfile.gettempdir(), os.path.basename(urlparse(download_url).path)
            )
            with open(file_path, "wb") as f:
                f.write(req.content)
            return file_path

    def install_update(self) -> bool:
        logging.info("Attempting to poll updates")
        file_path = self.download_update()
        logging.info("Successfully polled updates")
        if file_path:
            logging.info("Update available, attempting to install")
            try:
                subprocess.run(["dpkg", "-i", file_path])
                os.remove(file_path)
                logging.info(f"Successfully installed update at {file_path}")
                return True
            except PermissionError as e:
                logging.error(f"Update failed, insufficient permissions: {str(e)}")
                return False
        else:
            logging.info("No updates available")
