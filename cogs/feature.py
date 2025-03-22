from discord.ext import commands
import random

class feature(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=["latency"])
    async def ping(self, ctx): #**************** ping command *******************
        await ctx.message.delete()
        await ctx.send(f"**PONG!** Latency: {round(self.client.latency*1000)}ms")
    
    @commands.command(aliases=["guilds"])
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"Serving {str(len(self.client.guilds))} Servers")


    @commands.command(aliases=["users"])
    @commands.is_owner()
    async def members(self, ctx):
        await ctx.send(f"Serving {str(len(self.client.users))} Users")

    @commands.command(aliases=["pick",'spin'])
    async def choose(self, ctx, *,op1=None ): #*******************Choose Command**************
        if op1==None :
            
            await ctx.send("You forgot to give the options !")
        else :  
            op = op1.split()
            await ctx.send(f"**I choose `{random.choice(op)}`**")    

        
def setup(client):
    client.add_cog(feature(client))