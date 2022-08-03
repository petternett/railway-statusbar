# railway-statusbar
Statusbar application which moves a train according to your typing speed.

![Illustration of the application in a statusbar](images/status.png)

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


## Known issues
- Sometimes displays the message "Environment variable TERM not set"
- Might not keep still if your emoji scaling is off. This can be fixed in Polybar by scaling your emoji font, i.e. `font-1 = JoyPixels:scale=8`.
