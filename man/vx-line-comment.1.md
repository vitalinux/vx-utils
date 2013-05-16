% VX-LINE-COMMENT(1) Linux | Comment/uncomment a line in a configuration file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-line-comment - Comment/uncomment a line in a configuration file

SYNOPSIS
========
vx-line-comment [-h] -t TEXT -f FILE [-s {#,;}] [-q] [-c | -u]

DESCRIPTION
===========
This command facilitates the operations of comment/uncomment lines in text configuration files

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-t** _TEXT_, **--text** _TEXT_: text to comment/uncomment in file

**-f** _FILE_, **--file** _FILE_: file to comment/uncomment text

**-s** {**#**,**;**}, **--start** {**#**,**;**}: character to comment/uncomment text ("#" by default)

**-q**, **--quiet**: enable silence mode (no verbose)

**-c**, **--comment**: enable comment mode (default mode)

**-u**, **--uncomment**: enable uncomment mode

EXAMPLES
========
Comment all lines that starts with "127.0.1.1" with character "#" in file

    vx-line-comment --text "127.0.1.1" --file /etc/hosts --start "#"

Uncomment all lines that starts with "linea" in file (by default search character "#")

    vx-line-comment -u -t "linea" -f ~/test/prueba.txt

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
