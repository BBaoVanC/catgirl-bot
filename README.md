# catgirl
A (WIP) basic open-source discord bot containing tools for filtering specific words, as well as simplistic moderation commands. Used in my personal servers

## Features
- Commands:
    - Moderation:
        - warn
        - kick
        - ban
        - purge
        - getlogs
    - Content Filtering:
        - filterrole
        - filter add/remove
    - Info:
        - userinfo/info/user
        - avatar/pfp
        - botinvite/link
        - ping
        - jumbo/emote
        - sysinfo/stats
        - uptime
        - github/source/sourcecode
        - say/copy/mimic
    - Config:
        - prefix
        - modrole
- Tracks message edits/deletion
- Logs all messages sent (can be downloaded by moderators with the getlogs command)
- Reacts to messages containing specific content (try "neko" or "catgirl", as well as "gm" and "gn")

## Dependencies (pip install these):
    - psutil
    - python_env
    - discord_py

## To use:
1. Install python 3.9.1
2. Create a file called .env in this folder
3. Get the token of the discord bot (please google if you don't already know how to get this)
4. Add DISCORD_TOKEN=your_token
5. Add CLIENT_ID=your_client_id (or the botinvite command will not work properly)
4. Go to this directory and run `py catgirl.py`