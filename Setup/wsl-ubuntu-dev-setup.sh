#!/usr/bin/env bash

#
# This script installs the latest versions of Rust, Go, Ruby, Python, Node.js, and npm
# on a fresh Ubuntu installation. It fetches the latest version numbers
# for Go, Ruby, Python, Node.js, and npm from their respective websites and installs
# them accordingly. It also updates the repositories, installs required
# packages, and sets the appropriate environment variables.
#

# Update repositories and install required packages
sudo apt update && sudo apt upgrade
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME"/.cargo/env

# Install the latest version of Go
GO_LATEST=$(curl -s https://golang.org/dl/ | grep -oP 'go([0-9]+\.[0-9]+(\.[0-9]+)?).linux-amd64.tar.gz' | head -n 1)
wget https://golang.org/dl/$GO_LATEST
sudo tar -C /usr/local -xzf "$GO_LATEST"
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
source ~/.bashrc

# Install Python
curl https://pyenv.run | bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
PYTHON_LATEST=$(pyenv install -l | grep -oP '^\s+3\.[0-9]+\.[0-9]+$' | tail -1)
pyenv install "$PYTHON_LATEST"
pyenv global "$PYTHON_LATEST"

# Install Ruby
curl -sSL https://get.rvm.io | bash -s stable --ruby
source ~/.rvm/scripts/rvm
RUBY_LATEST=$(rvm list known | grep -oP '^\[ruby\]-3\.[0-9]+\.[0-9]+$' | tail -1 | tr -d '[]')
rvm install "$RUBY_LATEST"

# Install the latest version of Node.js and npm
curl -fsSL https://install-node.now.sh/lts | sudo bash