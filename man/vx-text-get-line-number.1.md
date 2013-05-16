% VX-TEXT-GET-LINE-NUMBER(1) Linux | Get line number in text occurrence in file
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-text-get-line-number - Get line number in text occurrence in file (find only first occurrence)

SYNOPSIS
========
vx-text-get-line-number [-h] -t TEXT -f FILE [-s] [-q]

DESCRIPTION
===========
This command gets line number of a text in configuration files.  Finds only first occurrence of text.

OPTIONS
=======
**-h**, **--help**: show help message and exit

**-t** _TEXT_, **--text** _TEXT_: text to search in file

**-f** _FILE_, **--file** _FILE_: file to search

**-s**, **--start**: text must be start line to match

**-q**, **--quiet**: enable silence mode (no verbose)

EXAMPLES
========
Search first line that starts with **line** text in file

    vx-text-get-line-number -t line -f ~/test/dummy.txt -s

Search first line with **line** text in file

    vx-text-get-line-number -t line -f ~/test/dummy.txt

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
