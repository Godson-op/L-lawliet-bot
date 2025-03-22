import random
import discord
from discord.ext import commands
import sqlite3
import openai
import os

# -------------------< VARIABLES >----------------------

default_prefix = "-"

statuses = ["Death", "with API"]

log_channel = 923574116320165898

status = random.choice(statuses)
white = discord.Color.from_rgb(255, 255, 255)

zongdic = {
    1: [1232, 12.80],
    2: [1355, 13.76],
    3: [1489, 14.72],
    4: [1633, 16],
    5: [1787, 16.69],
    6: [1951, 17.92],
    7: [2126, 19.20],
    8: [2310, 20.48],
    9: [2506, 21.76],
    10: [2711, 23.04],
    11: [2927, 24.32],
    12: [3153, 25.06],
    13: [3389, 27.20],
}

# --------------------------< Functions >------------------------


def wembed(text, ctx=None):
    embed = discord.Embed(colour=white, description=text)
    if ctx is not None:
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
    return embed


def bembed(description, title, ctx):
    if title is not None:
        embed = discord.Embed(
            colour=discord.Color.blue(), description=description, title=title
        )
    else:
        embed = discord.Embed(colour=discord.Color.blue(), description=description)

    if ctx is not None:
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
    return embed


def lc(client):
    log_channel = 923574116320165898
    log_channel = client.get_channel(log_channel)
    return log_channel


# -------------------------> get prefix from prefixes database
def get_prefix(self, ctx):
    db = sqlite3.connect("db")
    c = db.cursor()
    c.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {ctx.guild.id}")
    p = c.fetchone()
    if p:
        prefix = str(p[0])
    else:
        prefix = default_prefix
    db.commit()
    c.close()
    db.close()
    return commands.when_mentioned_or(prefix)(self, ctx)


# -------------------------> get ai_channel from ai_channels database
def get_ai_channel(ctx):
    db = sqlite3.connect("db")
    c = db.cursor()
    c.execute(f"SELECT ai_channel FROM ai_channels WHERE guild_id = {ctx.guild.id}")
    p = c.fetchone()
    if p:
        aic = p[0]
    else:
        aic = None
    db.commit()
    c.close()
    db.close()
    return aic


def del_ai(ctx):
    db = sqlite3.connect("db")
    c = db.cursor()
    c.execute(f"SELECT * FROM ai_channels WHERE guild_id = {ctx.guild.id}")
    p = c.fetchone()
    if p:
        c.execute(f"DELETE FROM prefixes WHERE guild_id = {ctx.guild.id}")
    db.commit()
    c.close()
    db.close()
