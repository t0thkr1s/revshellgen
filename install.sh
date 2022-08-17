#!/bin/bash

linux_install_with_package_manager() {
  # if the OS is debian/ubuntu use apt-get to install $1
    if [ -f /etc/debian_version ]; then
        sudo apt-get install -y $1
    # elif the OS is archlinux use pacman to install $1
    elif [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm $1
    # elif the OS is redhat/fedora use yum to install $1
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y $1
    else
        echo "OS not supported"
        exit 1
    fi
}

linux_update_package_manager(){
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
    elif [ -f /etc/arch-release ]; then
        sudo pacman -Syu
    elif [ -f /etc/redhat-release ]; then
        sudo yum update
    else
        echo "OS not supported"
        exit 1
    fi
}

# update the packager appropriately for the OS and architecture
if [ "$(uname)" == "Darwin" ]; then
    export PACKAGER="macosx"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    export PACKAGER="linux"
fi

# update the architecture appropriately for the OS and architecture
if [ "$(uname -m)" == "x86_64" ]; then
    export ARCH="amd64"
elif [ "$(uname -m)" == "i686" ]; then
    export ARCH="386"
fi

# if the var $PACKAGER is not set, exit with an error
if [ -z "$PACKAGER" ]; then
    echo "Unable to determine the packager for this OS and architecture."
    exit 1
else
# else call the appropriate package manager to install
    if [[ "$PACKAGER" == "linux" ]]; then
        echo 'linux package manager update...'
        linux_update_package_manager
        echo 'linux package manager install...'
        linux_install_with_package_manager python3
    elif [[ "$PACKAGER" == "macosx" ]]; then
        if [ -f /usr/local/bin/brew ]; then
            echo "Homebrew is already installed so brew update and brew upgrade"
            echo "Homebrew installation skipped."
            brew update
            brew install python@3.9 pipenv
        else
            echo "Homebrew is not installed. Installation of homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            echo "Now installing, brew update and install python@3.9 and pipenv..."
            brew update
            brew install python@3.9 pipenv
        fi
    fi
fi

# Install dependencies
# install python3 dependencies from requirements.txt
echo "Installing python3 dependencies from requirements.txt..."
pip3 install -r requirements.txt
# install to /opt directory
echo "Installing of revshellgen to /opt directory..."
sudo mkdir -p /opt/revshellgen
sudo cp -r commands /opt/revshellgen/
sudo cp  LICENSE /opt/revshellgen/
sudo cp  revshellgen.py /opt/revshellgen/
# sed change the shebang line to use '/usr/bin/python3' instead of '/usr/bin/env python3' of /opt/revshellgen/revshellgen.py
sudo sed -i '1s/^/#!/usr/bin/python3/' /opt/revshellgen/revshellgen.py
sudo chmod a+x /opt/revshellgen/revshellgen.py
sudo ln -s /opt/revshellgen/revshellgen.py /usr/local/bin/revshellgen
echo "Installation complete."