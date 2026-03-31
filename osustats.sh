#!/bin/bash
# replace the this dir \/ with the one where your osuStats.py and osustats.config files are
cd $HOME/Documents/OsuStats/
if [ -d "venv" ]; then
    source venv/bin/activate
    python osuStats.py $1 $2
else
    python -m venv venv
    pip install ossapi typing_utils
    source venv/bin/activate
    python osuStats.py $1 $2
fi