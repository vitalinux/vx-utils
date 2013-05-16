% VX-GCONF(1) Linux | Gconf operations wrapper
% Written by Jose Antonio Chavarría
% 2013-05-16

NAME
====
vx-gconf - Gconf operations wrapper

SYNOPSIS
========
vx-gconf change [-h] -k KEY [-v VALUE]
          [-t {string,int,float,bool,pair,list}]
          [-l {string,int,float,bool}] [-m] [-u]

vx-gconf daemon [-h] (--on | --off | -r)

vx-gconf load [-h] -f FILE

DESCRIPTION
===========
This command simplifies **gconftool-2** options

OPTIONS
=======
**--help**, **-h**: show help message and exit

* vx-gconf change

    **--key** _KEY_, **-k** _KEY_: key in GConf

    **--value** _VALUE_, **-v** _VALUE_: key value in GConf

    **--type** {string,int,float,bool,pair,list}, **-t** {string,int,float,bool,pair,list}: key type

    **--list-type** {string,int,float,bool}, **-l** {string,int,float,bool}: list type

    **--mandatory**, **-m**: mandatory values in GConf

    **--unset**, **-u**: enable unset key mode

* vx-gconf daemon

    **--on**: start GConf daemon

    **--off**: stop GConf daemon

    **--reload**, **-r**: reload GConf daemon

* vx-gconf load

    **--file** _FILE_, **-f** _FILE_: file to load in GConf

EXAMPLES
========
Change GConf mandatory property

    vx-gconf change --key "/apps/metacity/general/button_layout" --type string --value "menu:minimize,maximize,spacer,close" --mandatory

Change GConf default property

    vx-gconf change --key "/apps/panel3-applets/object_0/show_weather" --type bool --value "true"

Unset GConf mandatory property

    vx-gconf change --key "/apps/metacity/general/button_layout" --unset --mandatory

COPYRIGHT
=========
Copyright © 2013 Jose Antonio Chavarría. License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
========
**gconftool-2(1)**

**gconf-editor(1)**
