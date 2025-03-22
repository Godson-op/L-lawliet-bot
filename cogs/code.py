import discord


class code(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command
    async def code(self, ctx):
        embed = discord.embed(description="Here's how to format Python code on Discord:\n```py\nprint('Hello world!')\n```", title= "These are backticks, not quotes.", url='https://superuser.com/questions/254076/how-do-i-type-the-tick-and-backtick-characters-on-windows/254077#254077')
        ctx.send(embed = embed)

def setup(client):
    client.add_cog(code(client))