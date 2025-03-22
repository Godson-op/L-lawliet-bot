import discord
from discord.ext import commands, tasks
import os
import utils


# -----------------------> Client object
client = commands.Bot(
    command_prefix=utils.get_prefix,
    help_command=None,
    case_insensitive=True,
    intents=discord.Intents.all(),
)


# -------------------------> On Ready Event
@client.event
async def on_ready():
    loop.start()
    print(f"{client.user.name} is on the move!")
    await utils.lc(client).send(embed=utils.wembed(f"`{client.user.name} ACTIVE!`"))


# --------------------------> Loop Task
# @tasks.loop(minutes=100)
# async def loop():
#     await client.change_presence(activity=discord.Game(utils.status))


@tasks.loop(minutes=60)
async def loop():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{str(len(client.users))} Users | -help",
        )
    )


# _________________________>- COG LOAD -<_____________________________

# ------------> Auto Load all cogs on start
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"--> {filename} cog loaded")
        except Exception as e:
            print(f"--> Failed to load {filename}: {str(e)}")


# ---------------------------> Cog Load
@client.command(aliases=["load"])
@commands.is_owner()
async def on(ctx, cog):
    try:
        client.load_extension(f"cogs.{cog}")
        print(f"{cog} Loaded")
        lc = utils.lc(client)
        await lc.send(embed=utils.wembed(f"` {cog} Loaded !`"))
    except Exception as e:
        print(f"--> {cog} Failed to load: {str(e)}")


# ---------------------------> Cog Unload
@client.command(aliases=["unload"])
@commands.is_owner()
async def off(ctx, cog):
    try:
        client.unload_extension(f"cogs.{cog}")
        print(f"{cog} Removed")
        lc = utils.lc(client)
        await lc.send(embed=utils.wembed(f"`{cog} Removed`"))
    except Exception as e:
        print(f"--> {cog} Failed to load: {str(e)}")


# --------------------------> Cog Reload
@client.command(aliases=["update"])
@commands.is_owner()
async def reload(stx, cog=None):
    if cog is None:
        print("______--> UPDATING ALL FILES...")
        try:

            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    client.reload_extension(f"cogs.{filename[:-3]}")
                    print(f"--> {filename} cog Reloaded")
            lc = utils.lc(client)
            await lc.send(embed=utils.wembed("`Reload Success`"))
        except Exception as e:
            print(f"--> Failed to reload: {str(e)}")
    else:
        try:
            client.reload_extension(f"cogs.{cog}")
            lc = utils.lc(client)
            await lc.send(embed=utils.wembed(f"`Updated {cog}`"))
            print(f"`Updated {cog}`")
        except Exception as e:
            print(f"--> Failed to reload: {str(e)}")


# ___________________________________________________________

token = os.environ.get("TOKEN")

# alive()
if __name__ == "__main__":
    client.run(token)
