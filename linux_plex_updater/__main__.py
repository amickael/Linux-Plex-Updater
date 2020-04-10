import os
import time
import logging

from linux_plex_updater.service import UpdateService


def main():
    # Get and check parameters
    params = {
        "username": os.getenv("PLEX_USER"),
        "password": os.getenv("PLEX_PASS"),
        "host": os.getenv("PLEX_HOST", "http://localhost"),
        "port": os.getenv("PLEX_PORT", 32400),
    }
    missing_params = [key for key, val in params.items() if val is None]
    if missing_params:
        logging.error(f"Missing {', '.join(missing_params)}")
        exit()

    # Create service and poll every X seconds
    service = UpdateService(**params)
    while True:
        service.install_update()
        time.sleep(os.getenv("REFRESH_INTERVAL", 1800))


if __name__ == "__main__":
    main()
