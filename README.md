# Linux-Plex-Updater
Plex auto-updater for Debian-based systems

## 👶 Dependencies
> Note that these are typically pre-installed on most distributions
* [Python 3.6 or higher](https://www.python.org/downloads/)
* [Git SCM](https://git-scm.com/downloads)

## 🛠️ Installation
Run the following command to install or update:
```sh
sudo bash -c "$(curl -sSL https://raw.githubusercontent.com/amickael/Linux-Plex-Updater/master/install.sh?$(date +%s))"
```

## ⚙️ Configuration
To edit the service configuration update `/opt/linux-plex-updater/config` in your favorite text editor, such as:
```sh
nano /opt/linux-plex-updater/config
```

### Configuration Parameters

| Name | Description | Default |
| --- | --- | --- |
| PLEX_USER | Plex.tv username | N/A
| PLEX_PASS | Plex.tv password | N/A
| PLEX_HOST | Plex server host | http://localhost
| PLEX_PORT | Plex server port | 32400
| REFRESH_INTERVAL | Update check interval in seconds | 1800

After updating the config file remember to restart the service by running:
```sh
sudo systemctl restart linux-plex-updater.service
```
