% VX-FILE-GET-KEY(1) Linux | Read a variable in a configuration file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-file-get-key - Read a variable in a configuration file

SYNOPSIS
========
vx-file-get-key [-h] -k KEY -f FILE [-s { ,=,:}] [-q]

DESCRIPTION
===========
This command facilitates the operations of read keys in text configuration files (.ini, .conf files).  Only reads first key occurrence.

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-k** _KEY_, **--key** _KEY_: key to search in file

**-f** _FILE_, **--file** _FILE_: file to search

**-s** { ,=,:}, **--separator** { ,=,:}: character separator between key and value ("=" by default)

**-q**, **--quiet**: enable silence mode (no verbose)

EXAMPLES
========
Return **UTC** key value from **/etc/default/rcS** ('=' as separator)

    vx-file-get-key --key UTC --file /etc/default/rcS

Return **One** key value with ':' as separator

    vx-file-get-key -k One -s ':' -f ~/test/dummy.conf

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
