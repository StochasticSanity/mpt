#!/usr/bin/env bash

# secure-system-setup.sh
# Bash script to apply security measures on a machine.
# Author: Joseph Erdosy
#
# This script applies various security measures on the system, such as
# setting up a firewall, configuring Fail2Ban, and configuring SSH.
#
# Usage: ./secure-system-setup.sh

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Update the system and install necessary packages
apt-get update
apt-get upgrade -y
apt-get install -y ufw fail2ban unattended-upgrades logwatch apticron sysstat apparmor apparmor-utils

# Set up the firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw enable

# Set up fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Configure SSH to use key-based authentication and disable password authentication
sed -i 's/#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl reload sshd

# Configure automatic security updates
dpkg-reconfigure -plow unattended-upgrades

# Configure logwatch
echo "Range = yesterday" >> /etc/logwatch/conf/logwatch.conf

# Configure apticron
# apticron will be installed during the package installation

# Configure sysstat
sed -i 's/^ENABLED="false"/ENABLED="true"/' /etc/default/sysstat
sed -i 's/^HISTORY=7/HISTORY=14/' /etc/sysstat/sysstat
echo '*/15 * * * * root /usr/lib/sysstat/sa1 1 1' > /etc/cron.d/sysstat

# Install and enable AppArmor
systemctl enable apparmor
systemctl start apparmor

# Apply a set of default AppArmor profiles
aa-enforce /etc/apparmor.d/*bin*
