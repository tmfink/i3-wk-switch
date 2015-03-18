# Description

Switches workspaces in the [i3 window manager](https://i3wm.org/) like xmonad.
This script will always bring the requested workspace to the current monitor
("output" in i3's terminology). If the requested workspace is showing on another
monitor, then the current workspace and requested workspace will swap positions
with each other.


# Requirements

- [i3 window manager](https://i3wm.org/)
- [i3-py](https://github.com/ziberna/i3-py)


# Install

Just download
[i3-wk-switch.py](https://raw.githubusercontent.com/tmfink/i3-wk-switch/master/i3-wk-switch.py)
and modify your i3 config to call `i3-wk-switch.py` when the workspace switching
keys are pressed.


# Usage
```
Usage: i3-wk-switch.py WORKSPACE_NUM
```


# Example

Download script

```
cd ~/.i3
git clone https://github.com/tmfink/i3-wk-switch.git
```

Add keybindings to ~/.i3/config

```
# Switch to workspace like xmonad
set $x_switch exec --no-startup-id ~/.i3/i3-wk-switch/i3-wk-switch.py
bindsym $mod+1 $x_switch 1
bindsym $mod+2 $x_switch 2
bindsym $mod+3 $x_switch 3
bindsym $mod+4 $x_switch 4
bindsym $mod+5 $x_switch 5
bindsym $mod+6 $x_switch 6
bindsym $mod+7 $x_switch 7
bindsym $mod+8 $x_switch 8
bindsym $mod+9 $x_switch 9
bindsym $mod+0 $x_switch 10
```
