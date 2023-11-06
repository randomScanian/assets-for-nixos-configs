# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


theme = dict(bg="#282A36",
             cur="#44475A",
             fg="#F8F8F2",
             com="#6272A4",
             cyan="#8BE9FD",
             green="#50FA7B",
             orange="#FFB86C",
             pink="#FF79C6",
             purple="#BD93F9",
             red="#FF5555",
             yellow="#F1FA8C")

mod = "mod4"
terminal = "kitty"
myEmacs = "emacsclient -c -a 'systemctl --user start emacs'"

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "b", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "f", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "n", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "p", lazy.layout.up(), desc="Move focus up"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "b", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "f", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "n", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "p", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "b", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "f", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "n", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "p", lazy.layout.grow_up(), desc="Grow window eup"),
    
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "e", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "space", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord([mod],"w", [
        Key([mod], "w", lazy.spawn(myEmacs), desc='Emacs Dashboard'),
    ])
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
group_labels = ["WWW", "CHAT", "GAME LAUNCHER", "GAME", "DEV", "ELSE1", "ELSE2", "ELSE3", "AWAY",]
group_layouts = ["columns", "max", "columns", "columns", "columns", "columns", "columns", "columns", "columns"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([Key([mod],
                     i.name,
                     lazy.group[i.name].toscreen(),
                     desc="Switch to group {}".format(i.name)),
                 Key([mod, "control", "shift"],
                     i.name,
                     lazy.window.togroup(i.name, switch_group=True),
                     desc="Switch to & move focused window to group {}".format(i.name)),
                 Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                     desc="move focused window to group {}".format(i.name))])

layouts = [
    layout.Columns(border_focus=theme["purple"],
                   border_normal=theme["com"],
                   border_width=4,
                   margin = 8,
                   grow_amount=1,
                   fair=True,
                   new_client_position = "top",
                   ratio=0.5),
    layout.Max()]

widget_defaults = dict(
    font="sans",
    fontsize=14,
    padding=3,
    background=theme["bg"],
    foreground=theme["fg"],
    border_color=theme["com"],
    graph_color=theme["purple"],
    fill_color=theme["bg"],
    frequency=0.1,
)

extension_defaults = widget_defaults.copy()

screens = [Screen(top=bar.Bar([widget.GroupBox(disable_drag=True,
                                               scroll=False,
                                               inactive=theme["purple"],
                                               highlight_method="line"),
                               widget.Prompt(),
                               widget.Spacer(),
                               widget.Chord(chords_colors={"launch": (theme["red"], theme["fg"])},
                                            name_transform=lambda name: name.upper()),
                               widget.HDDBusyGraph(device="nvme0n1"),
                               widget.DF(visible_on_warn=False,
                                         format='({uf}{m}|{r:.0f}%)'),
                               widget.Sep(),
                               widget.CPUGraph(),
                               widget.CPU(),
                               widget.Sep(),
                               widget.Memory(format = "{MemUsed: .0f}{mm}/{MemTotal: .0f}{mm} = {MemPercent}%"),
                               widget.Sep(),
                               widget.Systray(),
                               widget.PulseVolume(),
                               widget.Sep(),
                               widget.Clock(format="%Y-%m-%d %a %H:%M:%S %p"),
                               widget.QuickExit(),
                               widget.CurrentLayout(),
                               ],
                              32))]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = False
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

wmname = "LG3D"
