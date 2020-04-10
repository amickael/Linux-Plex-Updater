#!/bin/bash

# Install Python venv
apt-get install python3-venv

# Ask and set variables
install_dir=/opt/linux-plex-updater
unit_file=linux-plex-updater.service

echo "Plex username: "
read -r plex_user

echo "Plex password: "
read -r plex_pass

echo "Plex host [localhost]: "
read -r plex_host
plex_host=${plex_host:-localhost}

echo "Plex port [32400]: "
read -r plex_port
plex_port=${plex_port:-32400}

echo "Polling interval (seconds) [1800]: "
read -r poll
poll=${poll:-1800}


# Set working dir
rm -r $install_dir; mkdir $install_dir || exit
cd $install_dir || exit

# Clone code
git clone https://github.com/amickael/Linux-Plex-Updater.git

# Create virtual environment and install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Write environment
sed -i "s/{{CWD}}/$install_dir/g" $unit_file
sed -i "s/{{CWD}}/$install_dir/g" environment
sed -i "s/{{PLEX_USER}}/$plex_user/g" environment
sed -i "s/{{PLEX_PASS}}/$plex_pass/g" environment
sed -i "s/{{PLEX_HOST}}/$plex_host/g" environment
sed -i "s/{{PLEX_PORT}}/$plex_port/g" environment
sed -i "s/{{PLEX_INTERVAL}}/$poll/g" environment

# Copy unit file, enable, and start
cp $unit_file /etc/systemd/system
systemctl enable $unit_file
systemctl start $unit_file