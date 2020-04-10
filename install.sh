#!/bin/bash

# Install Python venv
apt-get install python3-venv

# Ask and set variables
install_dir=/opt/linux-plex-updater
unit_file=linux-plex-updater.service
read -r -p "Plex username: " plex_user
read -r -p -s "Plex password: " plex_pass


# Set working dir
rm -r $install_dir; mkdir $install_dir || exit
cd $install_dir || exit

# Clone code
git clone https://github.com/amickael/Linux-Plex-Updater.git .

# Create virtual environment and install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Write environment
sed -i "s/{{PLEX_USER}}/$plex_user/g" environment
sed -i "s/{{PLEX_PASS}}/$plex_pass/g" environment

# Copy unit file, enable, and start
cp $unit_file /etc/systemd/system
systemctl stop $unit_file; enable $unit_file; start $unit_file