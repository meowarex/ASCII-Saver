#!/bin/bash

## Written by Claude 4.5 Haiku (I am tired and will rewrite myself soonTM)

# Simple media detection - if Playerctl or PipeWire audio is being played, don't launch screensaver
# Returns 0 if audio is playing, 1 if not (ignores chromium NON MPRIS players)

DEBUG=${1:-0}

# Check if PipeWire has active audio nodes (actual playback happening)
if command -v pw-dump &>/dev/null; then
    if [ "$DEBUG" = "1" ]; then
        echo "[MEDIA CHECK] Checking PipeWire for active playback..." >&2
    fi
    
    # Look for audio nodes that are in "running" state (actual playback)
    # pw-dump outputs nodes with state info - "running": true means active playback
    active_nodes=$(pw-dump 2>/dev/null | grep -c '"running": true')
    
    if [ "$DEBUG" = "1" ]; then
        echo "[MEDIA CHECK] Found $active_nodes active/running nodes" >&2
    fi
    
    # If we found running audio nodes, audio is playing
    if [ "$active_nodes" -gt 0 ]; then
        # Filter to only count actual audio playback, not system stuff
        # Check if any sink is actually outputting audio (has running nodes connected)
        if pw-dump 2>/dev/null | grep -A2 -B2 '"running": true' | grep -q '"type": "PipeWire:Interface:Node"'; then
            if [ "$DEBUG" = "1" ]; then
                echo "[MEDIA CHECK] AUDIO IS PLAYING (PipeWire) - screensaver blocked" >&2
            fi
            exit 0  # Audio is playing
        fi
    fi
fi

# Check playerctl - covers all MPRIS players including Tidal, Spotify, and web browsers
if command -v playerctl &>/dev/null; then
    if [ "$DEBUG" = "1" ]; then
        echo "[MEDIA CHECK] Checking playerctl (MPRIS) players..." >&2
    fi
    
    players=$(playerctl -l 2>/dev/null)
    while IFS= read -r player; do
        status=$(playerctl -p "$player" status 2>/dev/null)
        if [ "$DEBUG" = "1" ]; then
            echo "[MEDIA CHECK]   $player: $status" >&2
        fi
        if [ "$status" = "Playing" ]; then
            if [ "$DEBUG" = "1" ]; then
                echo "[MEDIA CHECK] AUDIO IS PLAYING (playerctl: $player) - screensaver blocked" >&2
            fi
            exit 0
        fi
    done <<< "$players"
fi

if [ "$DEBUG" = "1" ]; then
    echo "[MEDIA CHECK] NO AUDIO DETECTED - screensaver can launch" >&2
fi
exit 1  # No audio playing
