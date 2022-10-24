#!/usr/bin/env bash
#
OUTPUT="pdctf-dist.tar"

# CREATE ARCHIVE
tar -cvf "$OUTPUT" 

# UI
tar -rvf "$OUTPUT" web-app/public eel_app.py challenges

# CMDLINE
tar -rvf "$OUTPUT" ctf_control.py example_config.yaml

# PURPLE DOME
tar -rvf"$OUTPUT" app plugins systems/* requirements.txt

# MISC
tar -rvf "$OUTPUT" setup_requirements_ubuntu.sh run_ctf_app.sh CTF-README.md

gzip "$OUTPUT" 
