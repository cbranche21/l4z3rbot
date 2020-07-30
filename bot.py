# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MAX_TTS_MESSAGES = int(os.getenv('MAX_TTS_MESSAGES'))
TTS_ROLE = os.getenv('TTS_ROLE')

messages_count = {}

client = discord.Client()

@client.event
async def on_ready():
    global guild
    for x in client.guilds:
        if x.name == GUILD:
            guild = x
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    # Remove TTS roles from users
    tts_role = discord.utils.get(guild.roles, name = TTS_ROLE)
    for member in guild.members:
        if not member.bot:
            await member.add_roles(tts_role)

@client.event
async def on_message(message):
    if message.tts:
        member = message.author
        if discord.utils.get(member.roles, name = TTS_ROLE):
            if member.id in messages_count:
                messages_count[member.id] += 1
                if messages_count[member.id] >= MAX_TTS_MESSAGES:
                    tts_role = discord.utils.get(member.roles, name = TTS_ROLE)
                    await member.remove_roles(tts_role)
            else:
                messages_count[member.id] = 1

client.run(TOKEN)