#!/usr/bin/env bash

# user-setup.sh
# Bash script to set up new cloud machine with my prefered configuration.
# Author: Joseph Erdosy
#
# This script updates the OS, configures BASH-IT and Oh-my-ZSH, then starship terminal
# and tmux, enabling these for local users and root.
#
# Usage: ./ubuntu-config-setup.sh

# Update the Ubuntu OS
echo "Updating Ubuntu OS..."
sudo apt update && sudo apt upgrade -y

# Install git if not installed
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo apt install -y git
fi

# Install Bash-IT for all users using /etc/skel
echo "Installing Bash-IT..."
git clone --depth=1 https://github.com/Bash-it/bash-it.git /etc/skel/.bash_it
echo 'source $HOME/.bash_it/bash_it.sh' >> /etc/skel/.bashrc

# Install Oh-My-ZSH for all users using /etc/skel
echo "Installing Oh-My-ZSH..."
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended --skip-chsh
cp -r $HOME/.oh-my-zsh /etc/skel/
echo 'export ZSH=$HOME/.oh-my-zsh' > /etc/skel/.zshrc
echo 'source $ZSH/oh-my-zsh.sh' >> /etc/skel/.zshrc

# Install Fira Code Nerd Font
echo "Installing Fira Code Nerd Font..."
sudo apt install -y fonts-firacode

# Install Starship Terminal for all users using /etc/skel
echo "Installing Starship Terminal..."
curl -fsSL https://starship.rs/install.sh | sh -s -- --yes
echo 'eval "$(starship init bash)"' >> /etc/skel/.bashrc
echo 'eval "$(starship init zsh)"' >> /etc/skel/.zshrc

# Clone the tmux-config repository
echo "Cloning the tmux-config repository..."
git clone git@github.com:StochasticSanity/tmux-config.git

# Copy the tmux-config files to /etc/skel
echo "Copying tmux-config files to /etc/skel..."
cp tmux-config/.tmux.conf /etc/skel/
cp tmux-config/.tmux.conf.local /etc/skel/

# Remove the tmux-config directory
echo "Removing the tmux-config directory..."
rm -rf tmux-config

# Set zsh as the default shell for new users
echo "Setting zsh as the default shell for new users..."
sudo useradd -D -s /usr/bin/zsh

# Copy the configuration to the root user's home directory
echo "Copying configuration to root user's home directory..."
sudo cp -r /etc/skel/.bash_it /root/
sudo cp /etc/skel/.bashrc /root/
sudo cp -r /etc/skel/.oh-my-zsh /root/
sudo cp /etc/skel/.zshrc /root/
sudo cp /etc/skel/.tmux.conf /root/
sudo cp /etc/skel/.tmux.conf.local /root/

echo "All tasks completed successfully!"
