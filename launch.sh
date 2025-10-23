#!/bin/bash

# Launch ASCII Screen Saver
alacritty --class SSS \
  -o 'window.startup_mode="Fullscreen"' \
  -o 'font.size=15' \
  -e bash -c "cd /path/to/ASCII-Saver && source .venv/bin/activate && python3 main.py" &

# Save alacritty PID
echo $! > /tmp/sss.pid

