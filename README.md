# railway-statusbar
Statusbar application which moves a train according to your typing speed.

![Illustration of the application in a statusbar](status.png)

## Requirements
Requires Python and python-xlib.


## Installation

### Polybar
Add as a polybar module:
```
[module/railway]
type = custom/script
exec = "/usr/bin/python3 -u ~/path/to/railway.py"
tail = true
interval = 1
```

### i3bar
tbd
