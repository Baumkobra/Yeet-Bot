import discord 


client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Admin Rechte usen"))

@client.event
async def on_message(message):
    if message.author == client.user:
        await message.delete()

@client.event
async def on_message(message):
   pass

@client.event
async def on_reaction_add(reaction, user):
  pass