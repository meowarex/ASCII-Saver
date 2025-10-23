swayidle -w \
    timeout 60 '/path/to/launch.sh' \
    resume 'kill $(cat /tmp/sss.pid 2>/dev/null); rm -f /tmp/sss.pid'