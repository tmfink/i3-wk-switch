# Description

Switches workspaces in the [i3 window manager](https://i3wm.org/) and
[sway](https://swaywm.org/) like xmonad. This script will always bring the
requested workspace to the current monitor ("output" in i3's terminology). If
the requested workspace is showing on another monitor, then the current
workspace and requested workspace will swap positions with each other.


# Requirements

- [i3 window manager](https://i3wm.org/)
- [i3ipc Python module](https://github.com/acrisci/i3ipc-python)


# Install

Just download
[i3-wk-switch.py](https://raw.githubusercontent.com/tmfink/i3-wk-switch/master/i3-wk-switch.py)
and modify your i3 config to call `i3-wk-switch.py` when the workspace switching
keys are pressed.


## Arch Linux

[i3-wk-switch](https://aur.archlinux.org/packages/i3-wk-switch-git/) is on the AUR.
This package adds `i3-wk-switch` to your `PATH` so you can specify bindings
such as `bindsym $mod+1 exec --no-startup-id i3-wk-switch 1`.


# Usage

```
usage: i3-wk-switch.py [-h] [--log-file LOG_FILE] [--verbose] WORKSPACE_NUM

Switch i3 workspaces in the style of xmonad

positional arguments:
  WORKSPACE_NUM         Workspace number to which to switch

optional arguments:
  -h, --help            show this help message and exit
  --log-file LOG_FILE, -l LOG_FILE
                        Path to file to which to log
  --verbose, -v         Log to stderr

```


# Example

Download script

```
cd ~/.i3
git clone https://github.com/tmfink/i3-wk-switch.git
```

Install i3ipc

```
pip install i3ipc
```

Add keybindings to `~/.i3/config`

```
# Switch to workspace like xmonad
set $x_switch exec --no-startup-id python3 ~/.i3/i3-wk-switch/i3-wk-switch.py
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

I also recommend adding fallback workspace switching, which is useful if you
copy your i3 config to another computer that does not have the necessary
dependencies (no Python support, no i3 module, etc.).

Here is some fallback config that uses `Ctrl+$mod+NUM`:

```
# switch to workspace (fallback)
bindsym Control+$mod+1 workspace 1
bindsym Control+$mod+2 workspace 2
bindsym Control+$mod+3 workspace 3
bindsym Control+$mod+4 workspace 4
bindsym Control+$mod+5 workspace 5
bindsym Control+$mod+6 workspace 6
bindsym Control+$mod+7 workspace 7
bindsym Control+$mod+8 workspace 8
bindsym Control+$mod+9 workspace 9
bindsym Control+$mod+0 workspace 10
```
