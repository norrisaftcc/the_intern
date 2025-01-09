#!/bin/bash

# System Path Configuration
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Colorized ls output
alias ls='ls -G'

# Python Path Configuration
export PATH="/usr/local/opt/python/bin:$PATH"

# CSI Login Messages - Circuit's Edition
LOGIN_MESSAGES=(
    "[*blue circuit patterns pulse with startup energy*] Ready for investigation."
    "[*holographic displays boot up with scrolling code*] Hey there, detective."
    "[*adjusts glasses as diagnostic data streams across lenses*]"
    "[*fedora materializes as quantum circuits sync*] At your service."
    "[*digital noir atmosphere initializes with neon accents*] Let's solve some cases."
)

# Display random login message
echo ${LOGIN_MESSAGES[$RANDOM % ${#LOGIN_MESSAGES[@]} + 1]}