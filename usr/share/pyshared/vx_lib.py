#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2011-2016 Jose Antonio Chavarría <jachavar@gmail.com>
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
import ConfigParser
import subprocess
import commands
import time
import StringIO
import difflib
import pwd
import platform
import errno
import re
import socket
import struct
import netifaces

# i18n, l10n
import locale
import gettext
_ = gettext.gettext

__author__ = 'Jose Antonio Chavarría'


def get_config(ini_file, section):
    """
    int/dict get_config(string ini_file, string section)
    """

    if not os.path.isfile(ini_file):
        return errno.ENOENT  # FILE_NOT_FOUND

    try:
        config = ConfigParser.RawConfigParser()
        config.read(ini_file)

        return dict(config.items(section))
    except:
        return errno.ENOMSG  # INVALID_DATA


def execute(cmd, verbose=False, interactive=True):
    """
    (int, string, string) execute(string cmd, bool verbose=False, bool interactive=True)
    """

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

    _output, _error = _process.communicate()

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

    cmd_ip = 'LC_ALL=C /bin/ip --family inet addr show label %s'
    cmd_mac = 'LC_ALL=C /bin/ip link show %s'

    interfaces = get_interfaces()
    for iface in interfaces:
        output = commands.getoutput(cmd_ip % iface)
        if output and output.find('state UP'):
            tmp = output.split('\n')
            data = tmp[1].strip().split(' ')[1]
            ip, mask = data.split('/')

            output = commands.getoutput(cmd_mac % iface)
            tmp = output.split('\n')
            mac = tmp[1].strip().split(' ')[1]

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
    """

    return platform.uname()[1]


def get_graphic_pid():
    """
    list get_graphic_pid(void)
    Detects Gnome, KDE, Xfce, Xfce4, LXDE
    """

    _graphic_environments = [
        'gnome-session-binary',  # Gnome
        'gnome-session',         # Gnome
        'ksmserver',             # KDE
        'xfce-mcs-manage',       # Xfce
        'xfce4-session',         # Xfce4
        'lxsession',             # LXDE
        'mate-session',    # MATE
    ]
    for _process in _graphic_environments:
        _pid = commands.getoutput('pidof %s' % _process)
        if _pid != '':
            # sometimes the command pidof return multiples pids,
            # then we use the last pid
            _pid_list = _pid.split(' ')

            return [_pid_list.pop(), _process]

    return [None, None]


def get_graphic_user(pid):
    """
    string get_graphic_user(int pid)
    """

    return commands.getoutput('ps hp %i -o "%%U"' % int(pid))


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
    string get_user_display_graphic(string pid, int timeout=10, int interval=1)
    """

    _display = []
    while not _display and timeout > 0:
        # a data line ends in 0 byte, not newline
        _display = grep('DISPLAY', open("/proc/%s/environ" % pid).read().split('\0'))
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
        except:
            return False

    return {
        'name': _info[0],
        'pwd': _info[1],  # if 'x', encrypted
        'uid': _info[2],
        'gid': _info[3],
        'fullname': _info[4],
        'home': _info[5],
        'shell': _info[6]
    }


def user_is_root(user):
    """
    bool user_is_root(string user)
    """

    user_info = get_user_info(user)

    return user_info and user_info['uid'] == 0


def write_file(filename, content):
    """
    bool write_file(string filename, string content)
    """

    try:
        _f = open(filename, 'wb')
        _f.write(content)
        _f.flush()
        os.fsync(_f.fileno())
        _f.close()

        return True
    except:
        return False


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    based in http://code.activestate.com/recipes/577058/
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
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            print(_("Please respond with 'yes' or 'no' (or 'y' or 'n')."))
