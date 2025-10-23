# ASCII Saver | OMARCHY Screensaver Port

A faithful port of the **OMARCHY OS screensaver** for **KDE Plasma** and other Linux distributions.

**This is a remake of the original OMARCHY screensaver from [OMARCHY OS](https://omarchy.org/). All visual effects and core concept are inspired by the OMARCHY project.**

---

## What is OMARCHY?

[OMARCHY OS](https://omarchy.org/) is a unique opinionated tiling desktop environment made by the Legendary [DHH](https://dhh.dk)!!

This project just provides an easy setup for KDE and other Desktop Environments to use the `terminaltexteffects` library to create the screensaver.

---
## Batteries

**Python 3.7 & Pip/Pipx** - Language and Package Manager
**Linux** - The OS (Works on windows but only in the terminal window & no playback check)
**Alacritty** - Terminal (works in others if modified `launch.sh`)
**swayidle** - Package for Screen Saver on Idle
**playerctl** - Media player control (prevents screensaver during playback)

## Setup

### 1. Install Dependencies

Install `Alacritty`, `swayidle`, and `playerctl` from the AUR or the Extra Repo

Arch: `sudo pacman -S alacritty swayidle playerctl`

### 2. Install Project

```bash
git clone https://github.com/meowarex/ascii-saver
cd ASCII-Saver
pip install -r requirements.txt --break-system-packages
```

### 3. Add Custom Content

Edit `content.txt` with your own ASCII art: [ASCII Generator](https://patorjk.com/software/taag/#p=display&f=Delta+Corps+Priest+1&t=MEOWAREX&x=none&v=4&h=4&w=80&we=false)

If no `content.txt` exists Somehow.. the screensaver uses a default placeholder.

### 4. Update Paths, Timeouts and Font Size in `launch.sh` & `autostart.sh`

**Launch.sh**
```Bash
#!/bin/bash

# Launch ASCII Screen Saver
alacritty --class SSS \
  -o 'window.startup_mode="Fullscreen"' \
  -o 'font.size=15' \
        # Here! ^^
  -e bash -c "cd /path/to/ascii-saver && python3 main.py" &
         # Here! ^^^^^^^^   

# Save alacritty PID
echo $! > /tmp/sss.pid
```

**autostart.sh**
```Bash
swayidle -w \
    timeout 300 'if ! bash /path/to/ascii-saver/media_check.sh; then bash /path/to/ascii-saver/launch.sh; fi' \
     # Here ^^^            ^^^^^^^^                                       ^^^^^^^^
    resume 'kill $(cat /tmp/sss.pid 2>/dev/null); rm -f /tmp/sss.pid'
```
---

## Usage

### Quick Test
```bash
python3 main.py
```

Press `Ctrl+C` to exit.

---

## KDE Plasma Integration

Since KDE Plasma (as of 6.5) Still doesnt have support for custom Screen Savers, we will use swayidle in Auto Start.

1. Open **System Settings** → **Autostart** → **Add New**
2. Click **Login Script**
3. Select the `launch.sh` script:
4. And it should automagically work on next Boot <3

The `launch.sh` script handles fullscreen terminal launch and cleanup.

---

## Other Desktop Environments

This port is optimized for **KDE Plasma**. For other desktop environments (GNOME, Cinnamon, XFCE, etc.), you will need to:

- Modify `launch.sh` for your DE's terminal requirements

The core Python application will work on any Linux distribution, but system integration requires DE-specific configuration.

---

## Credits

- **Original Concept**: [OMARCHY OS Screensaver](https://omarchy.org/)
- **Effects Library**: [Terminal Text Effects](https://github.com/BradyBangasser/terminal-text-effects)