% VX-LINE-DELETE(1) Linux | Delete a line in a file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-line-delete - Delete a line in a file (only first occurrence)

SYNOPSIS
========
vx-line-delete [-h] -t TEXT -f FILE [-q]

DESCRIPTION
===========
This command facilitates the operations of delete lines in text configuration files.  Only deletes first text occurrence.

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-t** _TEXT_, **--text** _TEXT_: text to delete in file (all line)

**-f** _FILE_, **--file** _FILE_: file to delete line

**-q**, **--quiet**: enable silence mode (no verbose)

EXAMPLES
========
Delete text in silence mode (without output, only exit code)

    vx-line-delete --text "AllowUsers=root" --file /etc/ssh/sshd_config --quiet

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
