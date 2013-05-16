% VX-LINE-INSERT(1) Linux | Insert a text in a file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-line-insert - Insert a text in a file

SYNOPSIS
========
vx-line-insert [-h] -t TEXT -f FILE [-q] [-a | -l LINE]

DESCRIPTION
===========
This command facilitates the operations of insert lines in text configuration files

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-t** _TEXT_, **--text** _TEXT_: text to insert in file

**-f** _FILE_, **--file** _FILE_: file to insert line

**-q**, **--quiet**: enable silence mode (no verbose)

**-a**, **--append**: append text to the end of file if no line number exists (default mode)

**-l** _LINE_, **--line** _LINE_: append text at line number

EXAMPLES
========
Insert text at line 2 in silence mode (without output, only exit code)

    vx-line-insert --line 2 --text "127.0.1.1  PC00001.red.zaragoza.es" --file /etc/hosts --quiet

Insert text at the end of file

    vx-line-insert -t "last line" -f ~/test/dummy.txt

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
