from discord.ext import commands
import sqlite3
import utils

class custom_prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases= ['current_prefix','guild_prefix','server_prefix'])
    async def prefix(self, ctx):
        db=sqlite3.connect('db')
        c=db.cursor()
        c.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {ctx.guild.id}')
        p=c.fetchone()
        if p:
            prefix = str(p[0])
        else:
            prefix = utils.default_prefix
        db.commit()
        c.close()
        db.close()
        await ctx.send(
            f'**Current Server Prefix = ` {prefix} ` or You can @mention me to use commands**')


    #Change Prefix Command
    @commands.command(aliases=['setprefix'])
    @commands.has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new=utils.default_prefix):
        guild = ctx.guild.id
        if len(new) > 5:
            return await ctx.send('**Prefix need to be smaller then 5 characters**')
        db=sqlite3.connect('db')
        c=db.cursor()
        c.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {guild}')
        p=c.fetchone()
        if new == utils.default_prefix:
            if p:
                c.execute(f'DELETE FROM prefixes WHERE guild_id = {guild}')
                print(f'{ctx.guild} prefix deleted = set to default')
                await ctx.send(f'server prefix set to `{new}`')
                await utils.lc(self.client).send(embed=utils.bembed(f'`{ctx.guild}` Server Updated Prefix From`{p}` To `{new}`'))
            else:
                await ctx.send(f'server prefix is already default `{utils.default_prefix}`')
        else:
            if p:
                c.execute(f'UPDATE prefixes SET prefix =? WHERE guild_id = ?',(new,guild))
                await ctx.send(f'server prefix set to `{new}`')
                await utils.lc(self.client).send(embed=utils.bembed(f'`{ctx.guild}` Server Updated Prefix From`{p}` To `{new}`'))
                print(f'{ctx.guild} updated prefix to')
            else:
                c.execute(f'INSERT INTO prefixes(guild_id, prefix) VALUES(?,?)',(guild,new))
                await ctx.send(f'server prefix set to `{new}`')
                await utils.lc(self.client).send(embed=utils.bembed(f'`{ctx.guild}` Server Updated Prefix From `{utils.default_prefix}` To {new}'))
                print(f'{ctx.guild} now using custom prefix')
        db.commit()
        c.close()
        db.close()
        

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await utils.lc(self.client).send(embed=utils.bembed(f'Joined `{guild}` Server'))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await utils.lc(self.client).send(embed=utils.bembed(f'Left `{guild}` Server'))
        db=sqlite3.connect('db')
        c=db.cursor()
        c.execute(f'SELECT * FROM prefixes WHERE guild_id = {guild.id}')
        p=c.fetchone()
        c.execute(f'SELECT * FROM ai_channels WHERE guild_id = {guild.id}')
        q=c.fetchone()
        if p:
            c.execute(f'DELETE FROM prefixes WHERE guild_id = {guild.id}')
            print(f'Left *{guild}* (custom_prefix deleted)')
        if q:
            c.execute(f'DELETE FROM ai_channels WHERE guild_id = {guild.id}')
            print(f'Left *{guild}* (ai_channel delete)')
        
        
def setup(client):
    client.add_cog(custom_prefix(client))