% VX-FILE-SET-KEY(1) Linux | Replace a variable value in a configuration file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-file-set-key - Replace a variable value in a configuration file

SYNOPSIS
========
vx-file-set-key [-h] -k KEY -v VALUE -f FILE [-s { ,=,:}] [-a] [-q]

DESCRIPTION
===========
This command facilitates the operations of change keys values in text configuration files (.ini, .conf files).  Replaces all key occurrences.

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-k** _KEY_, **--key** _KEY_: key to replace in file

**-v** _VALUE_, **--value** _VALUE_: new value to key

**-f** _FILE_, **--file** _FILE_: file to search

**-s** { ,=,:}, **--separator** { ,=,:}: character separator between key and value ("=" by default)

**-a**, **--append**: append key and value to the end of file (if not exists)

**-q**, **--quiet**: enable silence mode (no verbose)

EXAMPLES
========
Set **timeout** key in silence mode (blank space as separator)

    vx-file-set-key --key 'timeout' --value '90;' --separator ' ' --file /etc/dhcp/dhclient.conf --quiet

Set key in file (append to the end of file if not exists)

    vx-file-set-key --key 'prepend domain-name-servers' --value '192.168.1.1;' --separator ' ' --file /etc/dhcp/dhclient.conf --append

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
