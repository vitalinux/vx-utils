# -*- coding: UTF-8 -*-

# Copyright (c) 2011-2020 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess
import time
import difflib
import pwd
import platform
import errno
import re
import select
import fcntl
import socket
import struct
import netifaces
import configparser

# i18n, l10n
import locale
import gettext
_ = gettext.gettext

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'


def get_config(ini_file, section):
    """
    int/dict get_config(string ini_file, string section)
    """

    if not os.path.isfile(ini_file):
        return errno.ENOENT  # FILE_NOT_FOUND

    try:
        config = configparser.RawConfigParser()
        config.read(ini_file)

        return dict(config.items(section))
    except:
        return errno.ENOMSG  # INVALID_DATA


def execute(cmd, verbose=False, interactive=True):
    """
    (int, string, string) execute(
        string cmd,
        bool verbose=False,
        bool interactive=True
    )
    """
    _output_buffer = ''

    if verbose:
        print(cmd)

    if interactive:
        _process = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash'
        )
    else:
        _process = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash',
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if verbose:
            fcntl.fcntl(
                _process.stdout.fileno(),
                fcntl.F_SETFL,
                fcntl.fcntl(
                    _process.stdout.fileno(),
                    fcntl.F_GETFL
                ) | os.O_NONBLOCK,
            )

            while _process.poll() is None:
                readx = select.select([_process.stdout.fileno()], [], [])[0]
                if readx:
                    chunk = _process.stdout.read()
                    if chunk and chunk != '\n':
                        print(chunk)
                    _output_buffer = '{}{}'.format(_output_buffer, chunk)

    _output, _error = _process.communicate()

    if not interactive and _output_buffer:
        _output = _output_buffer

    if isinstance(_output, bytes) and not isinstance(_output, str):
        _output = str(_output, encoding='utf8')
    if isinstance(_error, bytes) and not isinstance(_error, str):
        _error = str(_error, encoding='utf8')

    return _process.returncode, _output, _error


def get_interface_ip(iface):
    """
    string get_interface_ip(string)
    returns a dotted-quad string
    for Linux systems only!!!
    """
    _addresses = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in _addresses:
        return _addresses[netifaces.AF_INET][0]['addr']

    return ''  # empty string


def get_interfaces():
    _interfaces = netifaces.interfaces()
    if 'lo' in _interfaces:
        _interfaces.remove('lo')  # loopback interface is not interesting

    return _interfaces


def get_lan_ip():
    """
    string get_lan_ip(void)
    returns only first occurrence (without verify state)
    """
    _ret = ''
    _interfaces = get_interfaces()
    for _interface in _interfaces:
        if get_interface_ip(_interface) != '':
            _ret = _interface
            break

    return _ret


def ipv4_cidr_to_netmask(bits):
    """
    Convert CIDR bits to netmask
    http://nme.pl/en/2010/05/ipv4-cidr-to-netmask-in-python
    """

    netmask = ''
    for i in range(4):
        if i:
            netmask += '.'
        if bits >= 8:
            netmask += '%d' % (2**8 - 1)
            bits -= 8
        else:
            netmask += '%d' % (256 - 2**(8 - bits))
            bits = 0

    return netmask


def get_net_device_info():
    devices = dict()

    cmd_ip = 'LC_ALL=C /bin/ip --family inet addr show label {}'
    cmd_mac = 'LC_ALL=C /bin/ip link show {}'

    interfaces = get_interfaces()
    for iface in interfaces:
        output = subprocess.getoutput(cmd_mac.format(iface))
        if output and output.find('state UP') != -1:
            tmp = output.split('\n')
            mac = tmp[1].strip().split(' ')[1]

            output = subprocess.getoutput(cmd_ip.format(iface))
            tmp = output.split('\n')
            data = tmp[0].strip().split(' ')[1]
            ip, mask = data.split('/')

            devices[iface] = {
                'ip': ip,
                'mac': mac,
                'mask': ipv4_cidr_to_netmask(int(mask)),
                'cidr_mask': mask
            }

    return devices


def get_gateway():
    """
    string get_gateway(void)
    reads the default gateway directly from /proc
    from http://stackoverflow.com/questions/2761829/
    python-get-default-gateway-for-a-local-interface-ip-address-in-linux
    """
    with open('/proc/net/route') as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack('<L', int(fields[2], 16)))


def get_hostname():
    """
    string get_hostname(void)
    Returns only hostname (without domain)
    """

    return platform.node().split('.')[0]


def get_graphic_pid():
    """
    list get_graphic_pid(void)
    Detects Gnome, KDE, Xfce, Xfce4, LXDE, Unity, MATE
    """

    _graphic_environments = [
        'gnome-session-binary',  # Gnome & Unity
        'gnome-session',         # Gnome
        'ksmserver',             # KDE
        'xfce-mcs-manage',       # Xfce
        'xfce4-session',         # Xfce4
        'lxsession',             # LXDE
        'mate-session',          # MATE
    ]
    for _process in _graphic_environments:
        _pid = subprocess.getoutput('pidof -s {}'.format(_process))
        if _pid:
            return [_pid, _process]

    return [None, None]


def get_graphic_user(pid=0):
    """
    string get_graphic_user(int pid=0)
    """

    if not pid:
        pid = get_graphic_pid()[0]
        if not pid:
            return ''

    _user = subprocess.getoutput('ps hp {} -o "%U"'.format(pid))
    if _user.isdigit():
        # ps command not always show username (show uid if len(username) > 8)
        _user_info = get_user_info(_user)
        if _user_info is False:  # p.e. chroot environment
            return 'root'
        else:
            return _user_info['name']

    return _user


def grep(pattern, source):
    """
    http://casa.colorado.edu/~ginsbura/pygrep.htm
    py grep command
    sample command: grep("^x", dir())
    syntax: grep(regexp_string, list_of_strings_to_search)
    """

    expr = re.compile(pattern)
    return [elem for elem in source if expr.match(elem)]


def get_user_display_graphic(pid, timeout=10, interval=1):
    """
    string get_user_display_graphic(
        string pid,
        int timeout=10,
        int interval=1
    )
    """

    _display = []
    while not _display and timeout > 0:
        # a data line ends in 0 byte, not newline
        _display = grep(
            'DISPLAY',
            open('/proc/{}/environ'.format(pid)).read().split('\0')
        )
        if _display:
            _display = _display[0].split('=').pop()
            return _display

        time.sleep(interval)
        timeout -= interval

    if not _display:
        _display = ':0.0'

    return _display


def compare_lists(a, b):
    """
    list compare_lists(list a, list b)
    returns ordered diff list
    """

    _result = list(difflib.unified_diff(a, b, n=0))
    # clean lines... (only package lines are important)
    # http://docs.python.org/tutorial/controlflow.html#for-statements
    for _line in _result[:]:
        if _line.startswith('+++') or _line.startswith('---') \
                or _line.startswith('@@'):
            _result.remove(_line)

    return sorted(_result)


def compare_files(a, b):
    """
    list compare_files(a, b)
    returns ordered diff list
    """

    if not os.path.isfile(a) or not os.path.isfile(b):
        return None

    # U - open for input as a text file with universal newline interpretation
    # http://www.python.org/dev/peps/pep-0278/
    _list_a = open(a, 'U').readlines()
    _list_b = open(b, 'U').readlines()

    return compare_lists(_list_a, _list_b)


def get_user_info(user):
    """
    bool/list get_user_info(string user)
    """

    try:
        _info = pwd.getpwnam(user)
    except KeyError:
        try:
            _info = pwd.getpwuid(int(user))
        except KeyError:
            return False

    return {
        'name': _info[0],
        'pwd': _info[1],  # if 'x', encrypted
        'uid': _info[2],
        'gid': _info[3],
        # http://en.wikipedia.org/wiki/Gecos_field
        'fullname': _info[4].split(',', 1)[0],
        'home': _info[5],
        'shell': _info[6]
    }


def user_is_root(user=None):
    """
    bool user_is_root(string user=None)
    user parameter is kept for backward compatibility
    """

    return os.geteuid() == 0


def write_file(filename, content):
    """
    bool write_file(string filename, string content)
    """

    _dir = os.path.dirname(filename)
    if not os.path.exists(_dir):
        try:
            os.makedirs(_dir, 0o0777)
        except OSError:
            return False

    _file = None
    try:
        _file = open(filename, 'wb')
        try:
            _file.write(bytes(content))
        except TypeError:
            _file.write(bytes(content, encoding='utf8'))
        _file.flush()
        os.fsync(_file.fileno())
        _file.close()

        return True
    except IOError:
        return False
    finally:
        if _file is not None:
            _file.close()


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Based in http://code.activestate.com/recipes/577058/
    """
    valid = {
        _("yes"): "yes", _("y"): "yes",
        _("no"): "no", _("n"): "no"
    }
    if default is None:
        prompt = ' %s ' % _("[y/n]")
    elif default == "yes":
        prompt = ' %s ' % _("[Y/n]")
    elif default == "no":
        prompt = ' %s ' % _("[y/N]")
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            print(_("Please respond with 'yes' or 'no' (or 'y' or 'n')."))
