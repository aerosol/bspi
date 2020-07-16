# bspi

Automatic desktop renamer for bspwm.
Similar to [btops](https://github.com/cmschuetz/btops) but interfaces via subprocesses rather than UNIX sockets and focuses on icons.

Recognizes clients and renames desktops accordingly to a pre-configured
FontAwesome icon set. Works with polybar.

![scrot](https://user-images.githubusercontent.com/173738/72690918-348f7d80-3b21-11ea-979e-4c70228eb958.png)

## Prerequisites:

bspwm (duh), xprop, python3, FontAwesome etc.

## Installation:

Run `bspi_listen &` in your `bspwmrc`.

Icons are configured via `bspi.ini` - you may maintain your own copy and use it with `bspi_listen --config path/to/bspi.ini`.
The `_other` key is a fallback for all mismatched window names.

```ini
[Icons]
dolphin = 
chromium = 
firefox = 
signal = 
slack = 
spotify = 
termite = 
urxvt = 
tilix = 
alacritty = 
kitty = 
code-oss = 
_other = 
```

For polybar, make sure the fonts are configured in `polybar/config`, e.g.

```
font-3 = Font Awesome 5 Free:pixelsize=20;3
font-4 = Font Awesome 5 Free Solid:pixelsize=20;3
font-5 = Font Awesome 5 Brands:pixelsize=20;3
```

# TODO

  - [ ] tests
  - [ ] docs
  - [ ] screencast gif
  - [ ] external configuration
  
 # Known issues
 
[Polybar Format Tags](https://github.com/polybar/polybar/wiki/Formatting#format-tags) won't work for colored icons, [bspwm truncates desktop names at 32 bytes](https://github.com/baskerville/bspwm/blob/df7c6cc7813deec854922a5c2cc56a6b2e7cc8d2/src/types.h#L268).
