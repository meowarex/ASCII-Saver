#!/bin/bash

# Launch ASCII Screen Saver
alacritty --class saver \
  -o 'window.startup_mode="Fullscreen"' \
  -o 'font.size=15' \
  -e bash -c "cd /path/to/ascii-saver && python3 main.py" &

# Save alacritty PID
echo $! > /tmp/saver.pid

