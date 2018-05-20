"""
Selena - A bot for Discord.
"""
import os
import shutil
import subprocess
import sys

from discord.ext.commands import Bot


TOKEN = os.environ.get("DTOKEN")
BOT = Bot(description="Selena", command_prefix="selena")
NSFW = ["440356939256299530", "447524267199037451", "447524102505496576"]
LOG_CHANNEL = ""


@BOT.event
async def on_ready():
    """On bot start."""
    global LOG_CHANNEL
    LOG_CHANNEL = BOT.get_channel("447547444566163457")


@BOT.event
async def on_message(m):
    """Log all messages."""
    if m.author.bot:
        return

    if m.channel.id in NSFW:
        return

    await BOT.send_message(LOG_CHANNEL, log_msg(m, "MSG"))


@BOT.event
async def on_message_delete(m):
    """Log deleted messages."""
    if m.author.bot:
        return

    if m.channel.id in NSFW:
        return

    await BOT.send_message(LOG_CHANNEL, log_msg(m, "DELETED"))


@BOT.event
async def on_message_edit(_, m):
    """Log deleted messages."""
    if m.author.bot:
        return

    if m.channel.id in NSFW:
        return

    await BOT.send_message(LOG_CHANNEL, log_msg(m, "EDITED"))


def log_msg(m, msg_type):
    """Log message in specific format."""
    return "__%s__ [#%s] **@%s** \n```%s %s```" \
           % (msg_type, m.channel, m.author, m.content,
              ", ".join([attach["url"] for attach in m.attachments]))


def main():
    """Main function."""
    if not TOKEN:
        print("error: Token not found.")
        sys.exit(1)

    if shutil.which("git"):
        print("info: Updating bot.")
        subprocess.run(["git", "pull"])

    BOT.run(TOKEN)


main()
