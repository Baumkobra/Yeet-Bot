
import discord 
import heuriger
import os
from discord import Embed
from datetime import date
from keep_alive import keep_alive
from heuriger import Heuriger, fetch,pretty_fetch
dateformat = "%d.%m"
client = discord.Client()

@client.event
async def on_ready():
    print("ready")
    await client.change_presence(activity=discord.Game(name="HeurigerDon"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mes = message.content.lower()
    
    if not mes.startswith("?"):
        return
    
    if mes.startswith("?heuriger"):
        now = date.today()
        data = fetch()
        embed = Embed(title = f"Offene Heuriger am {now.strftime(dateformat)}")
        for heuriger in data:
            heuriger:Heuriger
            embed.add_field(name=heuriger.name,value=f"{heuriger.adresse}\nNoch {heuriger.tagenochoffen} offen\nTel:{heuriger.telefonnummer}")
        await message.channel.send(embed=embed)



@client.event
async def on_reaction_add(reaction, user):
  pass
keep_alive()
client.run(os.getenv("TOKEN"))