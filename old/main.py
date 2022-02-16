import os
import discord
from keep_alive import keep_alive


infoar = {}
#tim, benni, marius, julian
botar = {"ops":[365840909826523136,520109320424259604,572876853698887701,534418233273352205]}

# "feld":[], "player":[], ""

emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣","🔄", "✅", "🚫"]

startfeld = [1, 2, 3,
             4, 5, 6,
             7, 8, 9]


def Eingabe(player, dcinp, feld):
    try:
        if int(dcinp) in feld:
            feld[int(dcinp) - 1] = player
            return check(feld)
        else:
            return None
    except ValueError:
        return None


def check(feld):
    # horizontal
    for x in range(3):
        if feld[x * 3] == feld[1 + x * 3] == feld[2 + x * 3]:
            return True
        # vertikal
        elif feld[x] == feld[3 + x] == feld[6 + x]:
            return True
        # diagonal
        elif feld[0] == feld[4] == feld[8]:
            return True
        elif feld[2] == feld[4] == feld[6]:
            return True
    else:
        return False


def getBoardString(board):
    output = ""
    prboard={}
        
    

    for i in range(9):
        if type(board[i]) == int:
          prboard[i] = emojis[i]
        else: 
          prboard[i] = str(board[i])
        if (i + 1) % 3 == 0 and i != 0:
            output += " |  " + str(prboard[i]) + "  |\n"
        else:
            output += " | " + str(prboard[i]) + "  "
    return output


client = discord.Client()
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Admin Rechte usen"))

@client.event
async def on_message(message):
    if message.author.id == 548986486079619073:
        await message.delete()


@client.event
async def on_message(message):
    async def printemoji(message):
        for emoji in emojis:
            await message.add_reaction(emoji)
        return
   
    mes = message.content
    mes = mes.lower()

    if message.author.id in botar["ops"] and mes.startswith("?"):
        ops_num = len(botar["ops"])
        if mes.startswith("?kick"):
            kickid = mes.split()[1]
            kickid = kickid[3:-1]
            kickname = await client.fetch_user(kickid)
            if not kickid in botar:
                botar[kickid] = {"approved_by":[]}
            if not message.author.id in botar[kickid]["approved_by"]:
                botar[kickid]["approved_by"].append(message.author.id)
            approved_kick = len(botar[kickid]["approved_by"])
            if approved_kick >= (ops_num*0.75):
                await message.guild.kick(kickname,reason="Kicked by Op")
                await message.channel.send(f"{kickname} wurde vom Server gekickt. {approved_kick}/{ops_num}")
                botar[kickid] = {"approved_by":[]}
            else:
                await message.channel.send(f"{message.author.nick} will {kickname} kicken. {approved_kick}/{ops_num}")

        elif mes.startswith("?ban"):
            banid = mes.split()[1]
            banid = banid[3:-1]
            banname = await client.fetch_user(banid)
            if not banid in botar:
                botar[banid] = {"approved_by":[]}
            if not message.author.id in botar[banid]["approved_by"]:
                botar[banid]["approved_by"].append(message.author.id)
            approved_ban = len(botar[banid]["approved_by"])
            if len(botar[banid]["approved_by"]) == len(botar["ops"]):
                await message.guild.ban(banname,reason="Banned by Op")
                await message.channel.send(f"{banname} wurde vom Server gebannt. {approved_ban}/{ops_num}")
                botar[banid] = {"approved_by":[]}
            else:
              await message.channel.send(f"{message.author.nick} will {banname} bannen. {approved_ban}/{ops_num}")


                
    if message.author == client.user:
        return
    else:
        if not message.channel.id in infoar:
            infoar[message.channel.id] = {}
        if not "Player2" in infoar[message.channel.id]:
            if (mes == "?ttplay" or mes == "?revanche") and not "Player1" in infoar[message.channel.id]:
                player1 = message.author
                await message.delete()
                embedVar = discord.Embed(title="Tic Tac Toe", description=f"{player1.nick} will Tic Tac Toe spielen.")
                message2 = await message.channel.send(embed=embedVar)
                await message2.add_reaction(emojis[-2])
                await message2.add_reaction(emojis[-1])
                infoar[message.channel.id] = {"Player1": player1, "Channel": message.channel, "Start_mes": message2}
@client.event
async def on_reaction_add(reaction, user):
    
    async def printemoji(message):
        for emoji in emojis:
          if emoji == "✅" or emoji == "🔄":
            pass
          else:
            await message.add_reaction(emoji)
        return


    if client.user == user:
        return
    else:
        message = reaction.message
        mes = reaction.emoji
        try:
            emoji_index = emojis.index(mes)
        except ValueError:
            return
        if not message.channel.id in infoar:
            infoar[message.channel.id] = {}
        else:
            if not "Player2" in infoar[message.channel.id]:
                if mes == "🔄" and not "Player1" in infoar[message.channel.id]:
                    player1 = user
                    embedVar = discord.Embed(title="Tic Tac Toe",
                                             description=f"{player1.nick} will Tic Tac Toe spielen.")
                    message2 = await message.channel.send(embed=embedVar)
                    await message2.add_reaction(emojis[-2])
                    await message2.add_reaction(emojis[-1])
                    await message.clear_reaction("🔄")
                    infoar[message.channel.id] = {"Player1": player1, "Channel": message.channel, "Start_mes": message2}
                    return
                elif mes == "✅" and "Player1" in infoar[message.channel.id] and infoar[message.channel.id][
                    "Player1"] != user and message.channel == infoar[message.channel.id]["Channel"]:
                    player2 = user
                    embedVar = discord.Embed(title="Tic Tac Toe",description=f"{player2.nick} ist dem Tic Tac Toe beigetreten.")
                    embedVar.add_field(name="Spielfeld", value=getBoardString([1, 2, 3, 4, 5, 6, 7, 8, 9]))
                    messagealt = infoar[message.channel.id]["Start_mes"]
                    await messagealt.edit(embed = embedVar)
                    await messagealt.clear_reaction("✅")
                    await messagealt.clear_reaction("🚫")
                    await printemoji(messagealt)
                    infoar[message.channel.id]["Player2"] = player2
                    infoar[message.channel.id]["tourns"] = 0
                    infoar[message.channel.id]["Feld"] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    infoar[message.channel.id]["Zug"] = 0
                    infoar[message.channel.id]["Start_mes"] = messagealt
                    
                  
                    return
                try:
                    if mes == "🚫" and user == infoar[message.channel.id]["Player1"] and message.channel == \
                            infoar[message.channel.id]["Channel"]:
                        infoar[message.channel.id] = {}
                        embedVar = discord.Embed(title="Tic Tac Toe", description=f"Die Spielanfrage wurde von {user.nick} abgebrochen")
                        await message.edit(embed=embedVar)
                        for emoji in emojis:
                          await message.clear_reaction(emoji)
                        await message.add_reaction("🔄")
                        infoar[message.channel.id]["Start_mes"] = message
                        return
                except TypeError and KeyError:
                    return
            elif "Player2" in infoar[message.channel.id] and message.channel == infoar[message.channel.id]["Channel"]:
                feld = infoar[message.channel.id]["Feld"]
                player1 = infoar[message.channel.id]["Player1"]
                player2 = infoar[message.channel.id]["Player2"]
                if (user != player1) and (user != player2):
                    await discord.Reaction.remove(reaction, user)
                    return
                if (mes == "🚫") and (user == infoar[message.channel.id]["Player1"] or user == infoar[message.channel.id]["Player2"]):
                    #Spielabbruch
                    infoar[message.channel.id] = {}
                    await discord.Reaction.remove(reaction, user)
                    embedVar = discord.Embed(title="Tic Tac Toe")
                    embedVar.add_field(name="Info", value=f"Das Spiel wurde von {user.nick} abgebrochen")
                    await message.edit(embed=embedVar)
                    for emoji in emojis:
                      await message.clear_reaction(emoji)
                    await message.add_reaction("🔄")

                    return
                mes_int = emojis.index(mes) + 1
                if not mes_int in range(1, 10):
                    await discord.Reaction.remove(reaction, user)
                    return
                if not mes_int in feld:
                    await discord.Reaction.remove(reaction, user)
                    return
                tourns = infoar[message.channel.id]["tourns"]
                if tourns == 0 and user == player1:
                    infoar[message.channel.id]["Zug"] += 1
                    infoar[message.channel.id]["tourns"] = 1
                    await discord.Reaction.remove(reaction, user)
                    check_true = Eingabe("❎", mes_int, feld)
                    embedVar = discord.Embed(title="Tic Tac Toe", description=f"{player2.nick}'s Zug")
                    embedVar.add_field(name="Spielfeld", value=getBoardString(feld))
                    await message.edit(embed=embedVar)
                    if check_true:
                        embedVar = discord.Embed(title="Tic Tac Toe")
                        embedVar.add_field(name="Spielfeld",value=getBoardString(feld) + f"{player1.nick} hat das Spiel gewonnen \n Revanche ?")
                        await message.edit(embed=embedVar)
                        for emoji in emojis:
                          await message.clear_reaction(emoji)
                        await message.add_reaction("🔄")
                        infoar[message.channel.id] = {}
                        return
                elif tourns == 1 and user == player2:
                    infoar[message.channel.id]["Zug"] += 1
                    infoar[message.channel.id]["tourns"] = 0
                    await discord.Reaction.remove(reaction, user)
                    check_true = Eingabe("🅾️", mes_int, feld)
                    embedVar = discord.Embed(title="Tic Tac Toe", description=f"{player1.nick}'s Zug")
                    embedVar.add_field(name="Spielfeld", value=getBoardString(feld))
                    await message.edit(embed=embedVar)
                    if check_true:
                        embedVar = discord.Embed(title="Tic Tac Toe")
                        embedVar.add_field(name="Spielfeld",
                                           value=getBoardString(feld) + f"{player2.nick} hat das Spiel gewonnen \n Revanche ?")
                        await message.edit(embed=embedVar)
                        for emoji in emojis:
                          await message.clear_reaction(emoji)
                        await message.add_reaction("🔄")
                        infoar[message.channel.id] = {}
                        return
                elif tourns == 0 and not user == player1:
                    await discord.Reaction.remove(reaction, user)
                elif tourns == 1 and not user == player2:
                    await discord.Reaction.remove(reaction, user)
                if infoar[message.channel.id]["Zug"] >= 9:
                    embedVar = discord.Embed(title="Tic Tac Toe", description=f"{player2.nick}'s Zug")
                    embedVar.add_field(name="Spielfeld", value=getBoardString(feld) + "Unentschieden \n nochmal ?")
                    await message.edit(embed=embedVar)
                    for emoji in emojis:
                      await message.clear_reaction(emoji)
                    await message.add_reaction("🔄")
                    infoar[message.channel.id] = {}
                    return
keep_alive()
client.run(os.getenv("TOKEN"))