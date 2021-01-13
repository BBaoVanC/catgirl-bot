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
        - sysinfo/stats
        - uptime
        - github/source/sourcecode
    - Misc:
        - say/copy/mimic
        - jumbo/emote
        - sayembed
    - Image:
        - neko
        - leo s/n
    - Config:
        - prefix
        - modrole
        - logging yes/no
        - logchannel
        - reactions yes/no

- Tracks message edits/deletion, and sends to the channel with the id set in the logchannel command
- Logs all messages sent (can be downloaded by moderators with the getlogs command)
- Reacts to messages containing specific content (try "neko" or "catgirl", as well as "gm" and "gn")

## Debug mode:
You may enable debug mode by setting DEBUG to yes in your .env file. This will give you access to the `takesnap` command (only useable by bot owner), which will take a snapshot of python's currently used memory, and log some output to console. It adds thread count and current thread info to the `sysinfo` command. Not intended for normal use, as the name suggests, it's for debugging

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