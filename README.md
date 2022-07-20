# Flashpoint's Suggested Tags
A system to mark tags from older curations based in title matches. FPFSS will also suggest tags in the future, and false positives here refine the terms we'll use.

1. Get `flashpoint.sqlite` on the scripts folder and run `getsql.py`
2. `docker compose run` on the root folder
2.1. The page's script checks if the game was added after the current Flashpoint version, because curations fom FPFSS are not tied to their exported id, update it or use a future date to ignore
3. `convertvotes.py` can insert voted tags from a exported sql into flashpoint.sqlite, both in the scripts folder

Todo prob automate this better