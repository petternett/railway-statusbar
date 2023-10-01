# railway-statusbar
Statusbar application for Polybar which moves a train according to your typing speed.
Works with X, probably also works on Wayland (needs testing).

![Illustration of the application in a statusbar](images/status.png)

Animated example:
![Animated illustration of the application](images/animated.gif) 

## Requirements
Requires Python, [pynput](https://pypi.org/project/pynput/) and [emoji](https://pypi.org/project/emoji/).


## Installation

1. Clone repo
2. Add railway.py script as a statusbar module:

### Polybar
Add as a polybar module:
```
[module/railway]
type = custom/script
exec = "/usr/bin/python3 -u ~/path/to/railway.py"
tail = true
```

### i3bar
tbd


## Known issues
- Might not keep still if your emoji scaling is off. This can be fixed in Polybar by scaling your emoji font, i.e. `font-1 = JoyPixels:scale=8`.


## Planned features
- Persistent storage of total km-counter
- Optional WPM counter
