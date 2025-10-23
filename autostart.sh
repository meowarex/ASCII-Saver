#!/bin/bash

swayidle -w \
    timeout 300 'if ! bash /path/to/ascii-saver/media_check.sh; then bash /path/to/ascii-saver/launch.sh; fi' \
    resume 'kill $(cat /tmp/saver.pid 2>/dev/null); rm -f /tmp/saver.pid'
