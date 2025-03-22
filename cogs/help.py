import discord
from discord.ext import commands

from utils import default_prefix


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["h"])
    async def help(
            self,
            ctx ,p: discord.Member=None):  #************************HELP Command******************
        author = ctx.message.author

        embed = discord.Embed(
            description=
            f"Must use prefix({default_prefix}) before each command \n Example: -ping \nor u can mention me with the command ",
            colour=discord.Color.blue())

        embed.set_author(
            name="-Help",
            icon_url=
            'https://cdn.discordapp.com/emojis/765808823788240917.gif?v=1',
            url = 'https://t.me/Death_Note_episodes')

        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/770131524016013322/919633076718546995/L.png"
        )

        embed.set_footer(text=author, icon_url=author.avatar.url)

        embed.add_field(name="Music Features",
                        value='''join - join's the channel
                        play [url/name]- plays song
                        stop/pause - pause the music
                        resume - resume the music
                        skip - skip current song
                        loop - loops the current song
                        playing/now - shows now playing song
                        queue - shows the queue
                        shuffle - shuffle the queue
                        remove [song no. in queue] - remove song from queue
                        ''')

        embed.add_field(
            name="gif [search]",
            value=
            'Returns a random gif by default. Also can be used with specific searchs',
            inline=True)

        embed.add_field(
            name='translate [word] [language]',
            value=
            'translate the word (only 1 word translation) if no language is given default will be hindi',
            inline=True)

        embed.add_field(
            name="choose [options]",
            value='choose one of the given options(seprated by spaces)',
            inline=True)

        embed.add_field(name="define [word]",
                        value='Returns defination',
                        inline=True)

        embed.add_field(name="wiki [word]",
                        value='Return wikipedia summary',
                        inline=True)

        embed.add_field(name="embed [messege]",
                        value='convert a normal messege to embeded messege',
                        inline=True)

        embed.add_field(name="clear [integer]",
                        value='delete [integer] no. of messeges',
                        inline=True)
        
        button = discord.ui.Button(label='Death Note', url='https://t.me/Death_Note_episodes')
        view = discord.ui.View()
        view.add_item(button)

        await ctx.message.delete()
        if p is None or p==author:
            await ctx.send(f"{author.mention}",embed=embed)  #send to author private message
        else:
            await ctx.send(f'{p.mention}',embed=embed)


def setup(client):
    client.add_cog(help(client))
