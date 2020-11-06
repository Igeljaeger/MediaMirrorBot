# MediaMirrorBot

A discord bot that automatically mirrors media posts from the fediverse to discord. Tested with mastodon and pleroma instances, has not been tested with misskey, but will probably work.

## Requirements

The python code provided depends on [mastodon.py](https://github.com/halcy/Mastodon.py) and [discord.py](https://github.com/Rapptz/discord.py) in addition to python3.

The bot takes input from several text files in the repository, which you will have to fill in yourself. Details of their expected contents and how to fill them out are provided below:

### discord\_channels.txt

List of discord text channel id's to mirror posts to, separated by newlines. Find this by right-clicking a text channel and copying the ID. You may need to enable developer mode in discord's 'appearance' settings to see this option.

### discord\_token.txt

Contains the token for your discord bot, this is NOT the bot's secret. Find this in the 'bot' page of your discord application.

### fedi\_user.txt

Contains the login token for the account this bot will use to access the fediverse. See [mastodon.py's documentation](https://mastodonpy.readthedocs.io/en/stable/) for information on how to obtain this token.

### fedi\_users.txt

List of id's of fediverse users to mirror posts from, separated by newlines. These id's can normally be found in the URL bar of a user's profile when viewed from a remote instance, through the adminFE or through the mastodon.py API. These are not to be confused with ActivityPub IDs.
