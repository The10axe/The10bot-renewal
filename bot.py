import discord
# Discord API Reference: https://discordpy.readthedocs.io/en/v1.3.4/api.html
import datetime
import asyncio
import random

client = discord.Client()
# Change this to change the prefix of the bot:
prefix = "/"

# This will play when bot is ready:
@client.event
async def on_ready():
    print('Logged in as '+ str(client.user))

# This will trigger when bot see a message.
# It will store every info about the message in the var "message"
@client.event
async def on_message(message):
	# We prevent the bot from triggering its own commands
	if message.author == client.user:
		return
	
	# The command help, that makes an embed fields about everything possible with the bot
	if message.content.startswith(prefix+'help'):
		print("/help done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		info = await client.application_info()
		async with message.channel.typing():
			if info.owner == message.author:
				embed = discord.Embed(title="Help Page", description="For Owner and for Dummies", color=message.author.color)
			else:
				embed = discord.Embed(title="Help Page", description="For Users and for Dummies", color=message.author.color)
			embed.add_field(name="Tooltips:", value="[something] = Optional, <something> = required", inline=False)
			embed.add_field(name="/help", value="This is what you just did!")
			embed.add_field(name="/time", value="Gives you the Bot's time.")
			embed.add_field(name="/info [user]", value="Gives you info about a user, if no user is given, gives info about you")
			embed.add_field(name="/rps <user>", value="Challenge another user to Rock Paper Scissors")
			embed.add_field(name="/ping", value="Gives the latency of the bot to Discord")
			embed.add_field(name="/bot", value="Gives information about the bot!")
			embed.add_field(name="/seek <ID>", value="Gives you info about a user, using their ID")
			embed.add_field(name="/crypto [-lang:<morse|binary|hexadecimal|octal>] [-time:<seconds>] [-force:<true|false>] [sentences]", value="Starts a game where you need to guess what's written in a language, if nothing is given, a convertion table will be displayed, if only a sentences is given, the game start with default rules which is 300s (5 minutes) and a random language.", inline=False)
			if info.owner == message.author:
				embed.add_field(name="/stop", value="Stop the bot!")
			embed.set_footer(text=str(message.author), icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		return
	
	# Just print out the time
	if message.content.startswith(prefix+'time'):
		print("/time done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			await message.channel.send("Il est: "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		return

	# Gives info about a user, if none is given, gives info about yourself.
	# Can give: ID, Time account is made, Username, User Profile Picture
	# If in a guild, will give: Nickname, Top role of the server, Color of the top role, status
	if message.content.startswith(prefix+'info'):
		print("/info done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			if len(message.mentions) == 0:
				embed = discord.Embed(title="Info about "+str(message.author), description=None, color=message.author.color)
				embed.set_thumbnail(url=message.author.avatar_url)
				embed.add_field(name="ID:", value=str(message.author.id), inline=False)
				embed.add_field(name="Came in Discord:", value=str(message.author.created_at)[:-3], inline=False)
				# embed.add_field(name="Activities:", value=str(message.author.activities))
				if message.guild != None:
					embed.add_field(name="Top role in this server:",value=str(message.author.top_role), inline=False)
					embed.add_field(name="Nickname:", value=str(message.author.display_name), inline=False)
					embed.add_field(name="Status:", value=str(message.author.status).capitalize(), inline=False)
					embed.add_field(name="Came in Guild:", value=str(message.author.joined_at)[:-3], inline=False)
			else:
				if message.mentions[0] == client.user:
					embed = discord.Embed(title="Info about "+str(message.mentions[0]), description=None, color=message.mentions[0].color, url="https://discord.com/api/oauth2/authorize?client_id=426478004298842113&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com&scope=bot")
				else:
					embed = discord.Embed(title="Info about "+str(message.mentions[0]), description=None, color=message.mentions[0].color)
				embed.set_thumbnail(url=message.mentions[0].avatar_url)
				embed.add_field(name="ID:", value=str(message.mentions[0].id), inline=False)
				embed.add_field(name="Came in Discord:", value=str(message.mentions[0].created_at)[:-3], inline=False)
				# embed.add_field(name="Activities:", value=str(message.mentions[0].activities))
				if message.guild != None:
					embed.add_field(name="Top role in this server:",value=str(message.mentions[0].top_role), inline=False)
					embed.add_field(name="Nickname:", value=str(message.mentions[0].display_name), inline=False)
					embed.add_field(name="Status:", value=str(message.mentions[0].status).capitalize(), inline=False)
					embed.add_field(name="Came in Guild:", value=str(message.mentions[0].joined_at)[:-3], inline=False)
		embed.set_footer(text=str(message.author), icon_url=message.author.avatar_url)
		await message.channel.send(content=None,tts=False,embed=embed)
		return

	# Owner only command, makes the bot shutdown
	if message.content.startswith(prefix+'stop'):
		print("/stop done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		info = await client.application_info()
		if info.owner == message.author:
			async with message.channel.typing():
				await message.channel.send("Good bye!")
			print("Waiting for log out!")
			await client.logout()
			print("Shutting down...")
			exit()
		else:
			return

	# A very basic Rock Paper Scissors
	if message.content.startswith(prefix+'rps'):
		print("/rps done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			if len(message.mentions) == 0:
				await message.channel.send("Please ping a player to play against.")
				return
			elif message.mentions[0] == client.user:
				await message.channel.send("I read mind like no one elses. ~~I mean, you literally play by telling me what you'll do.~~")
				return
			else:
				player = [message.author,message.mentions[0]]
				embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
				embed.add_field(name="Status",value="Waiting for "+str(player[1])+" to be ready (You have 5 minutes)",inline=False)
				host = await message.channel.send(content=None,tts=False,embed=embed)
				await host.add_reaction('✅')
				def check(reaction, user):
					return (user == player[1]) and (str(reaction.emoji) == '✅') and (reaction.message.id == host.id)
				try:
					reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
				except asyncio.TimeoutError:
					embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
					embed.add_field(name="Status",value="Battle Canceled",inline=False)
					await host.edit(content=None,tts=False,embed=embed)
					await host.clear_reaction('✅')
				else:
					await host.clear_reaction('✅')
					action = ["",""]
					scheme = ['✊','🖐','✌']
					i = 0
					for u in player:
						embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xffff00)
						embed.add_field(name="Status",value=str(u)+" is playing",inline=False)
						await host.edit(content=None,tts=False,embed=embed)
						if u.dm_channel == None:
							await u.create_dm()
						play = await u.dm_channel.send(content="It's your turn to play! You have 5 minutes!\n"+str(player[0])+" VS "+str(player[1]))
						for x in scheme:
							await play.add_reaction(x)
						def checkPlay(reaction, user):
							nonlocal action
							nonlocal i
							action[i] = str(reaction.emoji)
							return (user == player[i]) and (str(reaction.emoji) in scheme) and (reaction.message.id == play.id)
						try:
							reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=checkPlay)
						except asyncio.TimeoutError:
							embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
							embed.add_field(name="Status",value=str(u)+" failed to play in time",inline=False)
							await host.edit(content=None,tts=False,embed=embed)
							return
						else:
							i = i + 1
					if action[0] == action[1]:
						embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xffa500)
						status = "Tie"
					elif (action[0] == '🖐' and action[1] == '✊') or (action[0] == '✊' and action[1] == '✌') or (action[0] == '✌' and action[1] == '🖐'):
						embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0x00ff00)
						status = str(player[0])+" won!"
					else:
						embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0x00ff00)
						status = str(player[1])+" won!"
					embed.add_field(name="Status",value=status,inline=False)
					embed.add_field(name="Playback",value=action[0]+" VS "+action[1],inline=False)
					await host.edit(content=None,tts=False,embed=embed)
					await host.add_reaction('👏')
		return
	
	# Gives the bot's delay to Discord's server
	if message.content.startswith(prefix+'ping'):
		print("/ping done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			embed = discord.Embed(title="I saw chu!", description="Chu forgot to say \"Pong!\".", color=0x00ff00)
			embed.add_field(name="Ping:",value=str(round(client.latency,4)*1000)+"ms",inline=False)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		return
	
	# Gives some bot's info
	if message.content.startswith(prefix+'bot'):
		print("/bot done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			embed = discord.Embed(title="The10bot", description="An open source bot coded in Python", url="https://discord.com/api/oauth2/authorize?client_id=426478004298842113&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com&scope=bot")
			embed.add_field(name="Source Code",value=str('[Available on Github](https://github.com/The10axe/The10bot-renewal)'), inline=False)
			embed.add_field(name="Last Update", value="25/07/2020 - 16:00", inline=False)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			info = await client.application_info()
			embed.set_author(name="The10axe", url="https://github.com/The10axe", icon_url=info.owner.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		return

	# Get a user's info with ID
	if message.content.startswith(prefix+'seek'):
		print("/seek done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			seek = client.get_user(int(message.content[6:]))
			if seek == None:
				await message.channel.send("Aucun résultat trouvé")
			else:
				embed = discord.Embed(title="Info about "+str(seek), description=None, color=seek.color)
				embed.set_thumbnail(url=seek.avatar_url)
				embed.add_field(name="ID:", value=str(seek.id), inline=False)
				embed.add_field(name="Came in Discord:", value=str(seek.created_at)[:-3], inline=False)
				# embed.add_field(name="Activities:", value=str(message.author.activities))
				await message.channel.send(content=None,tts=False,embed=embed)
		return
	
	if message.content.startswith(prefix+'crypto'):
		print("/crypto done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		morse = ["·-","-···","-·-·", "-··","·","··-·","--·","····","··","·---","-·-","·-··","--","-·","---","·--·","--·-","·-·","···","-","··-","···-","·--","-··-","-·--","--··","·----","··---","···--","····-","·····","-····","--···","---··","----·","-----","   "]
		lettre = ["A", "B", "C", "D", "E", "F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"," "]
		binary = ["01000001","01000010","01000011","01000100","01000101","01000110","01000111","01001000","01001001","01001010","01001011","01001100","01001101","01001110","01001111","01010000","01010001","01010010","01010011","01010100","01010101","01010110","01010111","01011000","01011001","01011010","00110001","00110010","00110011","00110100","00110101","00110110","00110111","00111000","00111001","00110000","00100000"]
		hexa=["41","42","43","44","45","46","47","48","49","4A","4B","4C","4D","4E","4F","50","51","52","53","54","55","56","57","58","59","5A","31","32","33","34","35","36","37","38","39","30","20"]
		octal=["101","102","103","104","105","106","107","110","111","112","113","114","115","116","117","120","121","122","123","124","125","126","127","130","131","132","061","062","063","064","065","066","067","070","071","060","040"]
		traitement = message.content.split(" ")
		if len(traitement) == 1:
			embed = discord.Embed(title="Converting table for "+str(message.author), description="Part 1", color=message.author.color)
			embed.add_field(name="Allowed character",value="Binary | Octal | Hexadecimal\nMorse", inline=False)
			for x in range(0,24):
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binaire[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
			await message.channel.send(content=None,tts=False,embed=embed)
			embed = discord.Embed(title="Converting table for "+str(message.author), description="Part 2", color=message.author.color)
			for x in range(24,len(lettre)):
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binaire[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
			await message.channel.send(content=None,tts=False,embed=embed)
		else:
			await message.delete()
			# Getting args
			available_lang = ["morse","binary","hexadecimal","octal"]
			lang = random.choice(available_lang)
			time = 300
			sentence_start = None
			lock = False
			force = False
			for x in range(1,len(traitement)):
				if traitement[x].startswith("-"):
					if traitement[x].startswith("-lang:"):
						if traitement[x][6:] in available_lang:
							lang = traitement[x][6:]
					if traitement[x].startswith("-time:"):
						if str(int(traitement[x][6:])) == traitement[x][6:]:
							time = float(int(traitement[x][6:]))
							if time < 1 or time > 3600:
								time = 300
					if traitement[x].startswith("-force:"):
						if bool(traitement[x][7:].capitalize()) in [True, False]:
							force = bool(traitement[x][7:].capitalize())
				elif lock == False:
					sentence_start = x
					lock = True
			#Grabing sentence
			sentence = ""
			for x in range(sentence_start, len(traitement)):
				if x == len(traitement)-1:
					sentence = sentence + str(traitement[x])
				else:
					sentence = sentence + str(traitement[x]) + " "
			original = sentence.strip()
			sentence = sentence.upper().strip()
			#Converting to language
			encrypted = ""
			error = 0
			for x in range(0,len(sentence)):
				found = False
				if lang == "morse":
					for i in range(0,len(lettre)):
						if sentence[x] == lettre[i]:
							if (x == len(sentence)-1) or sentence[x] == " ":
								encrypted = encrypted + str(morse[i])
							elif sentence[x+1] == " ":
								encrypted = encrypted + str(morse[i])
							else:
								encrypted = encrypted + str(morse[i]) + " "
							found = True
				if lang == "binary":
					for i in range(0,len(lettre)):
						if sentence[x] == lettre[i]:
							if (x == len(sentence)-1):
								encrypted = encrypted + str(binary[i])
							else:
								encrypted = encrypted + str(binary[i]) + " "
							found = True
				if lang == "hexadecimal":
					for i in range(0,len(lettre)):
						if sentence[x] == lettre[i]:
							if (x == len(sentence)-1):
								encrypted = encrypted + str(hexa[i])
							else:
								encrypted = encrypted + str(hexa[i]) + " "
							found = True
				if lang == "octal":
					for i in range(0,len(lettre)):
						if sentence[x] == lettre[i]:
							if (x == len(sentence)-1):
								encrypted = encrypted + str(octal[i])
							else:
								encrypted = encrypted + str(octal[i]) + " "
							found = True
				if found == False:
					encrypted = encrypted + "? "
					error = error + 1
			if error == 0 or force == True:
				if error > 0:
						embed = discord.Embed(title="What's written?", description=str(message.author)+" has forced result", color=0x00ff00)
						embed.add_field(name="Language", value=lang.capitalize(), inline=False)
						embed.add_field(name="Error", value=str(error), inline=False)
						embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
						embed.add_field(name="Sentences", value="`"+original+"`",inline=False)
						await message.channel.send(content=None,tts=False,embed=embed)
						return
				else:
					embed = discord.Embed(title="What's written?", description=str(message.author)+" has started a game", color=message.author.color)
					embed.add_field(name="Language", value=lang.capitalize(), inline=False)
					embed.add_field(name="Time", value=str(time)+"s", inline=False)
					embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
					host = await message.channel.send(content=None,tts=False,embed=embed)
					def check(m):
						return m.content.upper() == sentence and m.channel == message.channel
					try:
						winner = await client.wait_for('message', timeout=time, check=check)
					except asyncio.TimeoutError:
						embed = discord.Embed(title="What's written?", description=str(message.author)+" has started the game", color=0xff0000)
						embed.add_field(name="Language", value=lang.capitalize(), inline=False)
						embed.add_field(name="Time", value="Finished", inline=False)
						embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
						embed.add_field(name="Sentences", value="`"+original+"`",inline=False)
						embed.add_field(name="Winner", value=str(client.user), inline=False)
						await host.edit(content=None,tts=False,embed=embed)
						return
					else:
						embed = discord.Embed(title="What's written?", description=str(message.author)+" has started the game", color=0x00ff00)
						embed.add_field(name="Language", value=lang.capitalize(), inline=False)
						embed.add_field(name="Time", value="Finished", inline=False)
						embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
						embed.add_field(name="Sentences", value="`"+original+"`",inline=False)
						embed.add_field(name="Winner", value=str(winner.author), inline=False)
						await host.edit(content=None,tts=False,embed=embed)
						return
			else:
				await message.channel.send(content="Message of "+message.author.mention+" is invalid: `"+str(message.content)+"`\n"+str(error)+" error(s) has been found",tts=False,embed=None)
				return

# A quick script to open the file having the bot token, get the token and launch the bot with the token
file = open("./settings/token.id", "r")
Token = file.readline()
file.close()
# print("Token: "+str(Token)) # Uncomment this line to see in the CMD what is your bot's current token
print("Discord Version is: "+str(discord.version_info.releaselevel)+" "+str(discord.__version__))
client.run(Token)