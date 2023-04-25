#!/usr/bin/env bash

# user-setup.sh
# Bash script to set up new users on a machine with specific configurations.
# Author: Joseph Erdosy
#
# This script creates new users, adds them to the sudo group, configures their shell,
# sets up their SSH keys, and disables login messages for the new users.
#
# Usage: ./ubuntu-user-setup.sh user1 user2 user3 ...

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Check if at least one user is provided
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 user1 user2 user3 ..."
  exit 1
fi

# Set up the SSH directory in /etc/skel
mkdir -p /etc/skel/.ssh
touch /etc/skel/.ssh/authorized_keys
chmod -R 0700 /etc/skel/.ssh

# Iterate over the provided users
for newuser in "$@"
do
  # Create a new user with a home directory and Zsh as the default shell
  useradd -m -s /usr/bin/zsh "$newuser"
  
  # Add the new user to the sudo group
  usermod -aG sudo "$newuser"

  # Configure the shell prompt with Starship for both Bash and Zsh
  echo 'eval "$(starship init bash)"' >> "/home/$newuser/.bashrc"
  echo 'eval "$(starship init zsh)"'  >> "/home/$newuser/.zshrc"

  # Set the ownership of the new user's home directory
  chown -R "$newuser:$newuser" "/home/$newuser"

  # Disable login messages for the new user
  touch "/home/$newuser/.hushlogin"
done