import json
import discord 
import os
from discord import Embed
from datetime import date
from heuriger import Heuriger, fetch,pretty_fetch
from uuid import uuid4

dateformat = "%d.%m"
INLINE = False



class Client(discord.Client):
    async def on_ready(client):
        print("ready")
        await client.change_presence(activity=discord.Game(name="HeurigerDon"))
        print(client.guilds)

        with open("members.json","r") as file:
            client.opdict:dict = json.load(file)
        client.kickdict = {}
        for g_key in client.opdict.keys():
            client.kickdict.update({g_key:{}})


    async def on_message(client,message:discord.Message):
        if message.author == client.user:
            return
            
        mes:str = message.content.lower()
        
        if not mes.startswith("?"):
            return
        guild :discord.Guild= message.guild
        channel:discord.TextChannel = message.channel
        g_key = guild.id.__str__()
        
        if mes.startswith("?heuriger"):
            print(f"{message.guild}|{message.author.name} fragt Heuriger ab. id: {message.id}")
            now = date.today()
            data = fetch()
            embed = Embed(title = f"Offene Heuriger am {now.strftime(dateformat)}")
            for heuriger in data:
                heuriger:Heuriger
                print(heuriger.telurl)
                tel = f"Tel:[{heuriger.telefonnummer}]({heuriger.telurl})\n" if heuriger.telefonnummer != "" else ""
                embed.add_field(name=f"{heuriger.name}",value=f"{heuriger.adresse}\nNoch {heuriger.tagenochoffen} offen\n{tel}[website]({heuriger.url})",inline=INLINE)
               
            await channel.send(embed=embed)
            print(f"{message.guild}|{message.author.name} handling erfolgreich. id: {message.id}" )

        elif mes.startswith("?banright"):
            #Member Rechte zum Kicken/Bannen geben
            if message.author.id != guild.owner_id:
                print(f"{message.author.display_name} is NOT the owner")
                return
            print(f"{message.author.display_name} IS the owner")    
           
            if "add" in mes.removeprefix("?banright"):
                try:
                    with open("members.json","r") as file:
                        data =  json.load(file)
                    for member in message.mentions:
                        member:discord.Member
                        
                        if not g_key in data:
                            data[g_key] = []
                            print(f"created new guild in members.json: {guild.name}")
                        if not member.id in data[g_key]:
                            data[g_key].append(member.id)
                            await channel.send(f"added new op to {guild.name} op list: {member.display_name}|{member.id.__str__()}")
                        else:
                            await channel.send(f"{member.display_name} is already in op list")
                    with open("members.json","w") as file:
                        json.dump(data,file, indent=3)
                        client.opdict = data
                except IndexError:
                    print("IndexError")
                    return
            elif "remove" in mes.removeprefix("?banright"):      
                try:
                    with open("members.json", "r") as file:
                        data = json.load(file)
                    for member in message.mentions:
                        if member.id in data[g_key]:
                            await channel.send(f"removing member {member.display_name}")
                            data[g_key].remove(member.id)
        
                    with open("members.json","w") as file:
                        json.dump(data,file, indent=3)
                        client.opdict = data
                except IndexError:
                    print("IndexError")
                    return
                    
        elif mes.startswith("?kick"):
            if message.author.id not in client.opdict[g_key]:
                await channel.send(f"{message.author.display_name} hat keine Rechte")
                return
            minimum_ops = len(client.opdict[g_key])
            try:
                for member in message.mentions:
                    if member.id in client.opdict[g_key]:
                        continue

                    if not member.id in client.kickdict[g_key]:
                        client.kickdict[g_key][member.id] = {"approved_by":[]}

                    if member.id in client.kickdict[g_key] and message.author.id not in client.kickdict[g_key][member.id]['approved_by']:
                        client.kickdict[g_key][member.id]["approved_by"].append(message.author.id)
                        print(f"{[client.get_user(op) for op in client.kickdict[g_key][member.id]['approved_by']]} wollen {member.display_name} kicken")
                        await channel.send(f"{[client.get_user(op) for op in client.kickdict[g_key][member.id]['approved_by']].__str__()} wollen {member.display_name} kicken")

                    if len(client.kickdict[g_key][member.id]["approved_by"]) == minimum_ops:
                        print(f"kicking {member.display_name} with {len(client.kickdict[g_key][member.id]['approved_by'])} votes")
                        await channel.send(f"kicking {member.display_name} with {len(client.kickdict[g_key][member.id]['approved_by'])} votes")
                        await member.kick()

            except IndexError:
                print("IndexError")
                return
            
            


Client().run(os.environ["TOKEN"])
