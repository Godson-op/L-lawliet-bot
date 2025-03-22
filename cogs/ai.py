from discord.ext import commands
import openai
import asyncio
import utils
import sqlite3
from decouple import config

my_secret = config('AiKey')

class ai(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['aichatbot',"Chatbot", 'AiChannel','remove_chatbot','removechatbot'])
    async def ai_channel(self,
                         message,
                         channel: commands.TextChannelConverter = None):
        server = message.guild.id
        channel_in_db = utils.get_ai_channel(message)
        if channel is None:
            if channel_in_db is None:
                await message.send(embed=utils.bembed(title='-AI ChatBot Inactive', description='-to enable chatbot in a `[channel]` use command `-Chatbot [channel]` ', ctx=message))
            else:
                utils.del_ai(ctx=message)
                await message.send(embed= utils.bembed('-AI Chatbot Removed', ctx=message))
        else:
            if not channel_in_db is None:
                try:
                    db=sqlite3.connect('db')
                    c=db.cursor()
                    c.execute(f'UPDATE ai_channels SET ai_channel =? WHERE guild_id = ?',(channel.id,server))
                    db.commit()
                    c.close()
                    db.close()
                    await message.send(embed= utils.bembed(description='to remove run command `-remove_chatbot`' ,title=f'AI Chatbot Connected in `{channel}`', ctx=message))
                except:
                    await message.send(embed= utils.bembed('Command Failed Please provide a valid text channel [channel id/name/mention]',title= 'Command Failed', ctx= message))
            else :
                try:
                    db=sqlite3.connect('db')
                    c=db.cursor()
                    c.execute(f'INSERT INTO ai_channels(guild_id, ai_channel) VALUES(?,?)',(server,channel.id))
                    db.commit()
                    c.close()
                    db.close()
                    await message.send(embed= utils.bembed(description='to remove run command `-remove_chatbot`' ,title=f'AI Chatbot Connected in {channel}', ctx=message))
                except:
                    await message.send(embed= utils.bembed('Command Failed Please provide a valid text channel [channel id/name/mention]',title= 'Command Failed', ctx= message))


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user == message.author:
            return
            
        channel_in_db = utils.get_ai_channel(ctx=message)
        if message.channel.id == channel_in_db:
            async with message.channel.typing():
                response =utils.gpt(message.content)
                await asyncio.sleep((len(response)) / 20)
            await message.reply(response)


def setup(client):
    client.add_cog(ai(client))
