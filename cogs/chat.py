import discord
from discord.ext import commands
import wikipedia
import time
from PyDictionary import PyDictionary
from urllib.parse import quote_plus


class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'
        self.add_item(discord.ui.Button(label='Click Here', url=url))


class chat(commands.Cog):
    def __init__(self, client):
        self.client = client

    ####### CLEAN COMMAND ######
    @commands.command(aliases=["clean"])
    async def clear(self, ctx, amount=10):
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send("**You dont have permissions!**")
        else:
            async with ctx.channel.typing():
                count = 0
                async for message in ctx.channel.history(limit=amount + 1):
                 count += 1
                await ctx.channel.purge(limit=amount + 1)
            await ctx.channel.send(f"{count-1} evidences removed")
            time.sleep(3)
            await ctx.channel.purge(limit=1)

    #****************wiki command *******************
    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, t):
        content = wikipedia.summary( t , santences = 2 , auto_suggest = True )
        embed = discord.Embed(title=t,
                              description=content,
                              colour=discord.Colour.blue())
        embed.set_footer(text=ctx.author,
                         icon_url=ctx.message.author.avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed,)

    @commands.command(aliases=["meaning_of", "def"])
    async def define(
            self,
            ctx, word='Stupid'):  #******************Define Command***************
        dic = PyDictionary(word)
        definition = dic.getMeanings()
        embed = discord.Embed(title=word, description=definition)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=['t'])
    async def translate(self,
                        ctx,
                        *,
                        c='try giving some text'):  
        x=c.split()
        lang = 'hi'
              
        dic = PyDictionary(x[0])              
        t = dic.translateTo(lang)
        embed = discord.Embed(title=t[1], description=x[0])
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # Google
    @commands.command(aliases=['g'])
    async def google(self, ctx: commands.Context, *, query: str):
        """Returns a google link for a query"""
        await ctx.send(f'Google Result for: `{query}`')

    @commands.command(aliases=["m"])
    async def embed(
        self,
        ctx,
        *,
        mess='Add the messege with the command to embed'
    ):  #-************************Embed Command*********************
        author = ctx.author
        embed = discord.Embed(description=mess, colour=discord.Color.blue())
        embed.set_author(name=author, icon_url=author.avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(chat(client))
