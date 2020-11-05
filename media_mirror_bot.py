import discord
import asyncio
import time
import re
from mastodon import Mastodon
from asyncio import run

# Contains the login token for the account this bot will use to access the fediverse
# See mastodon.py's documentation for how to obtain this token
# https://mastodonpy.readthedocs.io/en/stable/
fediClient = Mastodon(
    access_token='fedi_user.txt',
    api_base_url='https://fedi.valkyrie.world')

# Contains the token for your discord bot, this is NOT the bot's secret
# Find this in the 'bot' page of your discord application
discord_token = open('discord_token.txt', 'r').read().strip()

# List of discord text channel id's to mirror posts to, separated by newlines
# Find this by right-clicking a text channel and copying the ID.
# You may need to enable developer mode in discord's 'appearance' settings to see this option.
discord_channels = open('discord_channels.txt', 'r').read().splitlines()

# List of id's of fediverse users to mirror posts from, separated by newlines
# These id's can normally be found in the URL bar of a user's profile, or through the public API
fedi_users = open('fedi_users.txt', 'r').read().splitlines()
media_posts = []

# This regex strips HTML tags from post content
html_cleaner = re.compile('<.*?>')

# Newest post the bot has recieved
newest_id = None

# Returns True if a post is not a reply and has between 1 and 4 (inclusive) media attachments
def is_media_post(post):
    if post.account.id in fedi_users:
        if post.in_reply_to_id == None:
            if len(post.media_attachments) > 0:
                if len(post.media_attachments) <= 4:
                    return True
    return False

while True:
    # Check for new posts
    # Mastodon's streaming API does not work if the bot is hosted on a pleroma or misskey instance, so we're resorting to polling for compatibility reasons.
    # Mastodon.py's timeline_list is also not being used for similar reasons.
    # If you are hosting this on a mastodon instance, using timeline_list may produce better results, in which case, fedi_users can be provided as the first argument.
    new_posts = fediClient.timeline_public(
        since_id=newest_id)

    # If there are new posts, update the newest post the bot has seen
    if len(new_posts) > 0:
        newest_id = new_posts[0].id

    # Filter out ineligible posts
    media_posts = [n for n in new_posts if is_media_post(n)]

    # If there are eligible posts, mirror them to discord
    if len(media_posts) > 0:
        print("Found " + str(len(media_posts)) + " media posts")

        # Stopping a discord bot closes the active event loop
        # Create a new event loop every time this happens
        if asyncio.get_event_loop().is_closed():
            print("Event loop closed. Fixing...")
            asyncio.set_event_loop(asyncio.new_event_loop())

        # Construct a new client using the active event loop
        discord_client = discord.Client()

        # Callback when bot is ready to post
        @discord_client.event
        async def on_ready():
            print("Discord bot is ready.")
            print("Mirroring {} posts across {} text channels".format(len(media_posts), len(discord_channels)))
            for channel_id in discord_channels:
                # Mirror post to dedicated channels
                channel = await discord_client.fetch_channel(channel_id)
                for post in media_posts:
                    text = "Post from " + post.account.username + "\n" 
                    text += re.sub(html_cleaner, '', post.content) + "\n"
                    for content in post.media_attachments:
                        text += content.url + "\n"
                    await channel.send(text)

            await discord_client.close()

        discord_client.run(discord_token)

    # Wait 30 seconds to check for new posts
    # You may want to tweak this value depending on how active your instance's public timeline is
    time.sleep(30)

