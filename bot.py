import discord
# Discord API Reference: https://discordpy.readthedocs.io/en/v1.3.4/api.html
import datetime
import asyncio
import random
import urllib.request

startup = datetime.datetime.now()
last_logged = "None"

client = discord.Client()
# Change this to change the prefix of the bot:
prefix = "/"

# Loading every global vars
try:
	file = open("./settings/blacklist.id", "r")
except FileNotFoundError:
	temp = []
	file = open("./settings/blacklist.id", "w")
	file.writelines(temp)
	file.close()
else:
	file.close()
file = open("./settings/blacklist.id", "r")
blocked = file.readlines()
file.close()
for value in range(0,len(blocked)):
	blocked[value] = blocked[value].rstrip('\n')
print(blocked)

allowed = None
try:
	file = open("./command/ip.id", "r")
except FileNotFoundError:
	allowed = []
	file = open("./command/ip.id", "w")
	file.writelines(allowed)
	file.close()
else:
	file.close()
file = open("./command/ip.id", "r")
allowed = file.readlines()
file.close()
for value in range(0,len(allowed)):
	allowed[value] = allowed[value].rstrip('\n')

morse = ["·-","-···","-·-·", "-··","·","··-·","--·","····","··","·---","-·-","·-··","--","-·","---","·--·","--·-","·-·","···","-","··-","···-","·--","-··-","-·--","--··","·----","··---","···--","····-","·····","-····","--···","---··","----·","-----","   "]
lettre = ["A", "B", "C", "D", "E", "F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"," "]
binary = ["01000001","01000010","01000011","01000100","01000101","01000110","01000111","01001000","01001001","01001010","01001011","01001100","01001101","01001110","01001111","01010000","01010001","01010010","01010011","01010100","01010101","01010110","01010111","01011000","01011001","01011010","00110001","00110010","00110011","00110100","00110101","00110110","00110111","00111000","00111001","00110000","00100000"]
hexa=["41","42","43","44","45","46","47","48","49","4A","4B","4C","4D","4E","4F","50","51","52","53","54","55","56","57","58","59","5A","31","32","33","34","35","36","37","38","39","30","20"]
octal=["101","102","103","104","105","106","107","110","111","112","113","114","115","116","117","120","121","122","123","124","125","126","127","130","131","132","061","062","063","064","065","066","067","070","071","060","040"]

# This will execute when bot is ready:
@client.event
async def on_ready():
	print('Logged in as '+ str(client.user))
	global last_logged
	last_logged = datetime.datetime.now()

# This will execute whenever the bot enters a server.
@client.event
async def on_guild_join(guild):
	if guild.system_channel != None:
		info = await client.application_info()
		embed = discord.Embed(title="Welcome to me!", description="Thanks for adding me to your server and so trusting me!", color=0xffffff)
		embed.add_field(name="How to use me?", value="/help", inline=False)
		embed.add_field(name="Owner of the bot", value=str(info.owner), inline=False)
		await guild.system_channel.send(content=None,tts=False,embed=embed)

# This will trigger when bot see a message.
# It will store every info about the message in the var "message"
@client.event
async def on_message(message):
	global blocked
	global allowed

	# We prevent the bot from triggering its own commands, or triggering to message made by a blocked user
	if (message.author == client.user) or (str(message.author.id) in blocked):
		return
	
	# The command help, that makes an embed fields about everything possible with the bot
	if message.content.startswith(prefix+'help'):
		print("/help done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		info = await client.application_info()
		traitement = message.content.split(" ")
		page = 1
		if len(traitement) == 1:
			page = 1
		elif str(int(traitement[1])) == traitement[1]:
			page = int(traitement[1])
		if page < 1:
			page = 1
		elif page > 2:
			page = 2
		async with message.channel.typing():
			if info.owner == message.author:
				embed = discord.Embed(title="Help Page "+str(page), description="For Owner and for Dummies", color=message.author.color)
			else:
				embed = discord.Embed(title="Help Page "+str(page), description="For Users and for Dummies", color=message.author.color)
			embed.add_field(name="Tooltips:", value="[something] = Optional, <something> = required", inline=False)
			if page == 1:
				embed.add_field(name="/help [page]", value="This is what you just did!")
				embed.add_field(name="/time", value="Gives you the Bot's time.")
				embed.add_field(name="/info [user]", value="Gives you info about a user, if no user is given, gives info about you")
				embed.add_field(name="/rps <user>", value="Challenge another user to Rock Paper Scissors")
				embed.add_field(name="/ping", value="Gives the latency of the bot to Discord")
				embed.add_field(name="/bot", value="Gives information about the bot!")
				embed.add_field(name="/seek <ID>", value="Gives you info about a user, using their ID")
				embed.add_field(name="/sncf", value="The satanic invocation of a french train")
				embed.add_field(name="/wtn [-min:<value>] [-max:<value>] [-force:<true|false>] [-ttj:<value>] [-ttp:<value>] [user]", value="Begin a \"What's the number\" game, forcing will put all non ready player AFK, ttj is Time To Join, ttp is Time To Play")
				embed.add_field(name="/crypto [-lang:<morse|binary|hexadecimal|octal>] [-time:<seconds>] [-force:<true|false>] [sentences]", value="Starts a game where you need to guess what's written in a language, if nothing is given, a convertion table will be displayed, if only a sentences is given, the game start with default rules which is 300s (5 minutes) and a random language.", inline=False)
				if info.owner == message.author:
					embed.add_field(name="/stop", value="Stop the bot!")
					embed.add_field(name="/block <ID or user>", value="Blocks the user from using my commands!")
			elif page == 2:
				if (str(message.channel.id) in allowed) and (info.owner != message.author):
					embed.add_field(name="/mc", value="Show's the Minecraft's server IP")
				elif info.owner == message.author:
					embed.add_field(name="/mc [-toggle]", value="Show's the Minecraft's server IP")
				embed.add_field(name="/ttt [-self:<true|false>] <user>", value="Start a Tic-Tac-Toe game against someone")
				embed.add_field(name="/server", value="Gives info about the server you trigger the command in!")
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
				embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
				host = await message.channel.send(content=None,tts=False,embed=embed)
				await host.add_reaction('✅')
				def check(reaction, user):
					return (user == player[1]) and (str(reaction.emoji) == '✅') and (reaction.message.id == host.id)
				try:
					reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
				except asyncio.TimeoutError:
					embed = discord.Embed(title="Rock Paper Scissors", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
					embed.add_field(name="Status",value="Battle Canceled",inline=False)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
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
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
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
							embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
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
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					await host.add_reaction('👏')
		return
	
	# Gives the bot's delay to Discord's server
	if message.content.startswith(prefix+'ping'):
		print("/ping done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		global last_logged
		global startup
		async with message.channel.typing():
			embed = discord.Embed(title="I saw chu!", description="Chu forgot to say \"Pong!\".", color=0x00ff00)
			embed.add_field(name="Ping:",value=str(int(round(round(client.latency,4)*1000)))+"ms",inline=False)
			embed.add_field(name="Command time:", value=str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			embed.add_field(name="Start time:", value=str(startup.strftime("%d/%m/%Y %H:%M:%S")))
			embed.add_field(name="Logged in time:", value=str(last_logged.strftime("%d/%m/%Y %H:%M:%S")))
			embed.add_field(name="Global Uptime:", value=str(datetime.datetime.now()-startup))
			embed.add_field(name="Last Uptime:", value=str(datetime.datetime.now()-last_logged))
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		return
	
	# Gives some bot's info
	if message.content.startswith(prefix+'bot'):
		print("/bot done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		async with message.channel.typing():
			embed = discord.Embed(title="The10bot", description="An open source bot coded in Python", url="https://discord.com/api/oauth2/authorize?client_id=426478004298842113&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com&scope=bot")
			embed.add_field(name="Source Code",value=str('[Available on Github](https://github.com/The10axe/The10bot-renewal)'), inline=False)
			embed.add_field(name="Official Server", value=str('[Discord Invite](https://discord.gg/YHy8fVV)'), inline=False)
			embed.add_field(name="Current version", value="Stable")
			embed.add_field(name="Last Update", value="05/09/2020 - 15:10", inline=False)
			embed.add_field(name="Currently watching", value=str(len(client.guilds))+" servers", inline=False)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			info = await client.application_info()
			embed.set_author(name="The10axe", url="https://github.com/The10axe", icon_url=info.owner.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		return

	# Get a user's info with ID&
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
				embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
				await message.channel.send(content=None,tts=False,embed=embed)
		return
	
	# A game about encrypted messages
	if message.content.startswith(prefix+'crypto'):
		print("/crypto done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		global morse
		global lettre
		global binary
		global hexa
		global octal
		traitement = message.content.split(" ")
		if len(traitement) == 1:
			embed = discord.Embed(title="Converting table for "+str(message.author), description="Part 1", color=message.author.color)
			embed.add_field(name="Allowed character",value="Binary | Octal | Hexadecimal\nMorse", inline=False)
			for x in range(0,24):
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binary[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
			embed = discord.Embed(title="Converting table for "+str(message.author), description="Part 2", color=message.author.color)
			for x in range(24,len(lettre)):
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binary[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
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
						if traitement[x][6:].lower() in available_lang:
							lang = traitement[x][6:].lower()
					if traitement[x].startswith("-time:"):
						if str(int(traitement[x][6:])) == traitement[x][6:]:
							time = float(int(traitement[x][6:]))
							if time < 1 or time > 3600:
								time = 300
					if traitement[x].startswith("-force:"):
						if bool(traitement[x][7:].lower().capitalize()) in [True, False]:
							force = bool(traitement[x][7:].lower().capitalize())
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
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await message.channel.send(content=None,tts=False,embed=embed)
						return
				else:
					embed = discord.Embed(title="What's written?", description=str(message.author)+" has started a game", color=message.author.color)
					embed.add_field(name="Language", value=lang.capitalize(), inline=False)
					embed.add_field(name="Time", value=str(time)+"s", inline=False)
					embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
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
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await host.edit(content=None,tts=False,embed=embed)
						return
					else:
						embed = discord.Embed(title="What's written?", description=str(message.author)+" has started the game", color=0x00ff00)
						embed.add_field(name="Language", value=lang.capitalize(), inline=False)
						embed.add_field(name="Time", value="Finished", inline=False)
						embed.add_field(name="Encrypted sentences", value="`"+encrypted+"`",inline=False)
						embed.add_field(name="Sentences", value="`"+original+"`",inline=False)
						embed.add_field(name="Winner", value=str(winner.author), inline=False)
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await host.edit(content=None,tts=False,embed=embed)
						return
			else:
				await message.channel.send(content="Message of "+message.author.mention+" is invalid: `"+str(message.content)+"`\n"+str(error)+" error(s) has been found",tts=False,embed=None)
				return

	# SNCF commend
	if message.content.startswith(prefix+'sncf'):
		print("/sncf done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		if message.author.voice.channel != None:
			voice_chat = await message.author.voice.channel.connect(timeout=60)
			voice_chat.play(discord.FFmpegPCMAudio('./sound/SNCF.mp3'), after=None)
			while voice_chat.is_playing() == True:
				await asyncio.sleep(1)
			await voice_chat.disconnect()
			minutes = random.randint(5,360)
			if minutes < 60:
				messagea = "The TER train n°"+str(random.randint(10000,999999))+" is "+str(minutes)+" minutes late!"
			else:
				heures = 0
				while minutes > 59:
					heures = heures + 1
					minutes = minutes - 60
				if heures == 1:
					heure = "1 hour"
				else:
					heure = str(heures)+" hours"
				if minutes < 2:
					minute = str(minutes)+" minute"
				else:
					minute = str(minutes)+" minutes"
				messagea = "The TER train n°"+str(random.randint(1000,999999))+" is "+heure+" and "+minute+" late!"
			embed = discord.Embed(title="SNCF", description=messagea,color=0x000000)
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Logo_TER.svg/1920px-Logo_TER.svg.png")
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		elif message.author.voice.channel == None:
			minutes = random.randint(5,360)
			if minutes < 60:
				messagea = "The TER train n°"+str(random.randint(1000,999999))+" is "+str(minutes)+" minutes late!"
			else:
				heures = 0
				while minutes > 59:
					heures = heures + 1
					minutes = minutes - 60
				if heures == 1:
					heure = "1 hour"
				else:
					heure = str(heures)+" hours"
				if minutes < 2:
					minute = str(minutes)+" minute"
				else:
					minute = str(minutes)+" minutes"
				messagea = "The TER train n°"+str(random.randint(1000,999999))+" is "+heure+" and "+minute+" late!"
			embed = discord.Embed(title="SNCF", description=messagea,color=0x000000)
			embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Logo_TER.svg/1920px-Logo_TER.svg.png")
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
	
	# Number guessing game
	if message.content.startswith(prefix+'wtn'):
		print("/wtn done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		traitement = message.content.split(" ")
		mini = 0
		maxi = 10000
		force = True
		ttj = 300
		ttp = 300
		for x in range(1,len(traitement)):
			if traitement[x].startswith("-"):
				if traitement[x].startswith("-min:"):
					if str(int(traitement[x][5:])) == traitement[x][5:]:
						mini = int(traitement[x][5:])
						if mini < 0:
							mini = 0
				if traitement[x].startswith("-max:"):
					if str(int(traitement[x][5:])) == traitement[x][5:]:
						maxi = int(traitement[x][5:])
						if maxi < 0:
							maxi = 10000
				if traitement[x].startswith("-force:"):
					if bool(traitement[x][7:].lower().capitalize()) in [True, False]:
						force = bool(traitement[x][7:].lower().capitalize())
				if traitement[x].startswith("-ttj:"):
					if str(int(traitement[x][5:])) == traitement[x][5:]:
						ttj = int(traitement[x][5:])
						if (ttj < 10) or (ttj > 3600):
							ttj = 300
				if traitement[x].startswith("-ttp:"):
					if str(int(traitement[x][5:])) == traitement[x][5:]:
						ttp = int(traitement[x][5:])
						if (ttp < 10) or (ttp > 3600):
							ttp = 300
		if maxi == mini:
			await message.channel.send(content="Max is equal to min",tts=False,embed=None)
			return
		elif maxi < mini:
			swap = maxi
			maxi = mini
			mini = swap
		target = int(random.randint(mini,maxi))
		if len(message.mentions) == 0:
			embed = discord.Embed(title="What's the number?", description=str(message.author)+" has started a game", color=0xffff00)
			embed.add_field(name="Minimum", value=mini)
			embed.add_field(name="Maximum", value=maxi)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			host = await message.channel.send(content=None,tts=False,embed=embed)
			score = 0
			if message.author.dm_channel == None:
				await message.author.create_dm()
			play = await message.author.dm_channel.send(content=None,tts=False,embed=embed)
			ongoing = True
			while ongoing == True:
				def check(m):
					test = m.content
					try:
						int(test)
					except ValueError:
						test = -1
					else:
						test = int(test)
					return (test >= mini) and (test <= maxi) and (m.channel.id == message.author.dm_channel.id)
				try:
					played = await client.wait_for('message', timeout=300, check=check)
				except asyncio.TimeoutError:
					embed = discord.Embed(title="What's the number?", description=str(message.author)+" has finished a game", color=0xff0000)
					embed.add_field(name="Minimum", value=mini)
					embed.add_field(name="Maximum", value=maxi)
					embed.add_field(name="Score", value="Cancelled")
					embed.add_field(name="Number to find", value=target)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					ongoing = False
					return
				else:
					score = score + 1
					if int(played.content) == target:
						embed = discord.Embed(title="What's the number?", description=str(message.author)+" has finished a game", color=0x00ff00)
						embed.add_field(name="Minimum", value=mini)
						embed.add_field(name="Maximum", value=maxi)
						embed.add_field(name="Score", value=score)
						embed.add_field(name="Number to find", value=target)
						await play.edit(content=None,tts=False,embed=embed)
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await host.edit(content=None,tts=False,embed=embed)
						ongoing = False
						return
					elif int(played.content) > target:
						embed = discord.Embed(title="What's the number?", description=str(message.author)+" has started a game", color=0xffff00)
						embed.add_field(name="Minimum", value=mini)
						embed.add_field(name="Maximum", value=maxi)
						embed.add_field(name="Score", value=score)
						embed.add_field(name="Number to find", value="Less than "+str(played.content))
						await play.edit(content=None,tts=False,embed=embed)
					else: 
						embed = discord.Embed(title="What's the number?", description=str(message.author)+" has started a game", color=0xffff00)
						embed.add_field(name="Minimum", value=mini)
						embed.add_field(name="Maximum", value=maxi)
						embed.add_field(name="Score", value=score)
						embed.add_field(name="Number to find", value="More than "+str(played.content))
						await play.edit(content=None,tts=False,embed=embed)
		else:
			player = [message.author]
			ready = [False]
			afk = [False]
			for x in message.mentions:
				player.append(x)
				ready.append(False)
				afk.append(False)
			if len(player) > 21:
				await message.channel.send(content="Too many player invited",tts=False,embed=None)
			else:
				embed = discord.Embed(title="What's the number?", description=str(message.author)+" is preparing a game", color=0x0000ff)
				embed.add_field(name="Minimum", value=mini)
				embed.add_field(name="Maximum", value=maxi)
				for x in range(0,len(player)):
					if ready[x] == False:
						embed.add_field(name=str(player[x]), value="Not ready")
					else:
						embed.add_field(name=str(player[x]), value="Ready")
				embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
				host = await message.channel.send(content=None,tts=False,embed=embed)
				await host.add_reaction('✅')
				def check(reaction, user):
					return (user in player) and (str(reaction.emoji) == '✅') and (reaction.message.id == host.id)
				while (ready.count(True)+afk.count(True)) != len(player):
					try:
						reaction, user = await client.wait_for('reaction_add', timeout=float(ttj), check=check)
					except asyncio.TimeoutError:
						if (force == False) or (ready.count(True) == 0):
							embed = discord.Embed(title="What's the number?", description="A player didn't get ready", color=0xff0000)
							embed.add_field(name="Minimum", value=mini)
							embed.add_field(name="Maximum", value=maxi)
							embed.add_field(name="Number to find", value=target)
							for x in range(0,len(player)):
								if ready[x] == False:
									embed.add_field(name=str(player[x]), value="Not ready")
								else:
									embed.add_field(name=str(player[x]), value="Ready")
							embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
							await host.edit(content=None,tts=False,embed=embed)
							await host.clear_reaction('✅')
							return
						else:
							for x in range(0, len(player)):
								if ready[x] == False:
									afk[x] = True
					else:
						for x in range(0, len(player)):
							if player[x] == user:
								ready[x] = True
						embed = discord.Embed(title="What's the number?", description=str(message.author)+" is preparing a game", color=0x0000ff)
						embed.add_field(name="Minimum", value=mini)
						embed.add_field(name="Maximum", value=maxi)
						for x in range(0,len(player)):
							if ready[x] == False:
								embed.add_field(name=str(player[x]), value="Not ready")
							else:
								embed.add_field(name=str(player[x]), value="Ready")
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await host.edit(content=None,tts=False,embed=embed)
				await host.clear_reaction('✅')
				score = [0]
				finish = [False]
				number = [-1]
				for x in range(0,len(player)):
					score.append(0)
					finish.append(False)
					number.append(-1)
				while (finish.count(True)+afk.count(True)) != len(player):
					for x in range(0, len(player)):
						if (finish[x] == False) and (afk[x] == False):
							embed = discord.Embed(title="What's the number?", description="Game has started!", color=0xffff00)
							embed.add_field(name="Minimum", value=mini)
							embed.add_field(name="Maximum", value=maxi)
							embed.add_field(name="Current turn", value=str(player[x]))
							embed.add_field(name="Player that finished", value=str(finish.count(True)))
							embed.add_field(name="Player that went AFK", value=str(afk.count(True)))
							embed.add_field(name="Player that haven't guessed", value=str(len(player)-(afk.count(True)+finish.count(True))))
							embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
							await host.edit(content=None,tts=False,embed=embed)
							embed = discord.Embed(title="What's the number?", description="It's your turn!", color=0xffff00)
							embed.add_field(name="Minimum", value=mini)
							embed.add_field(name="Maximum", value=maxi)
							embed.add_field(name="Score", value=score[x])
							if number[x] != -1:
								if number[x] > target:
									embed.add_field(name="Number to find", value="Less than "+str(number[x]))
								else:
									embed.add_field(name="Number to find", value="More than "+str(number[x]))
							if player[x].dm_channel == None:
								await player[x].create_dm()
							await player[x].dm_channel.send(content=None,tts=False,embed=embed)
							def check(m):
								test = m.content
								try:
									int(test)
								except ValueError:
									test = -1
								else:
									test = int(test)
								return (test >= mini) and (test <= maxi) and (m.channel.id == player[x].dm_channel.id)
							try:
								played = await client.wait_for('message', timeout=float(ttp), check=check)
							except asyncio.TimeoutError:
								afk[x] = True
								await player[x].dm_channel.send(content="Looks like you went AFK!",tts=False,embed=None)
							else:
								score[x] = score[x] + 1
								number[x] = int(played.content)
								if number[x] == target:
									finish[x] = True
									await player[x].dm_channel.send(content="You nailed it but I'd have done better! ~~I mean, I'm the one that made up that number, right?~~",tts=False,embed=None)
								else:
									await player[x].dm_channel.send(content="Ok!",tts=False,embed=None)
				embed = discord.Embed(title="What's the number?", description="The game has ended", color=0x00ff00)
				embed.add_field(name="Minimum", value=mini)
				embed.add_field(name="Maximum", value=maxi)
				embed.add_field(name="Number to find", value=target)
				found_score = False
				place = 1
				place_str = "1st"
				for score_cible in range(0,max(score)+1):
					if found_score == True:
						place = place + 1
						buffer = str(place)
						if buffer[len(buffer)-1:] == "1":
							place_str = str(place)+"st"
						elif buffer[len(buffer)-1:] == "2":
							place_str = str(place)+"nd"
						elif buffer[len(buffer)-1:] == "3":
							place_str = str(place)+"rd"
						else:
							place_str = str(place)+"th"
						found_score = False
					for x in range(0,len(player)):
						if (score[x] == score_cible) and (afk[x] == False):
							embed.add_field(name=str(place_str)+" ("+str(score[x])+")", value=str(player[x]))
							found_score = True
				for x in range(0,len(player)):
					if afk[x] == True:
						embed.add_field(name="DNF", value=str(player[x]))
				embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
				await host.edit(content=None,tts=False,embed=embed)
				await host.add_reaction('👏')
				return

	# A command made to block someone for executing a bot's command, only the bot owner can block someone.
	if message.content.startswith(prefix+'block'):
		info = await client.application_info()
		if info.owner == message.author:
			if len(message.mentions) == 0: # Si on ne mentionne personne
				traitement = message.content.split(" ")
				if len(traitement) == 2:
					if str(traitement[1]) in blocked:
						blocked.remove(str(traitement[1]))
						file = open("./settings/blacklist.id", "w")
						for value in blocked:
							file.write(value+"\n")
						file.close()
						await message.channel.send("ID: "+str(traitement[1])+" unblocked successfully!")
					else:
						seek = client.get_user(int(traitement[1]))
						if seek != None:
							blocked.append(str(traitement[1]))
							file = open("./settings/blacklist.id", "w")
							for value in blocked:
								file.write(value+"\n")
							file.close()
							await message.channel.send("ID: "+str(traitement[1])+" blocked successfully!")
			else:
				if str(message.mentions[0].id) in blocked:
						blocked.remove(str(message.mentions[0].id))
						file = open("./settings/blacklist.id", "w")
						for value in blocked:
							file.write(value+"\n")
						file.close()
						await message.channel.send("ID: "+str(message.mentions[0].id)+" unblocked successfully!")
				else:
					blocked.append(str(message.mentions[0].id))
					file = open("./settings/blacklist.id", "w")
					for value in blocked:
						file.write(value+"\n")
					file.close()
					await message.channel.send("ID: "+str(message.mentions[0].id)+" blocked successfully!")
	
	# A command to show the IP of the Raspberry Pi hosting a Minecraft Server, this command cannot be executed outside of allowed channel.
	if message.content.startswith(prefix+'mc'):
		info = await client.application_info()
		traitement = message.content.split(" ")
		if len(traitement) == 1:
			if str(message.channel.id) in allowed:
				ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
				await message.channel.send(content=ip+":25565",tts=False,embed=None)
		else:
			if message.author == info.owner:
				for x in range(1,len(traitement)):
					if traitement[x].startswith("-"):
						if traitement[x].startswith("-toggle"):
							if str(message.channel.id) in allowed:
								allowed.remove(str(message.channel.id))
								await message.channel.send(content="/mc disallowed in this channel",tts=False,embed=None)
							else:
								allowed.append(str(message.channel.id))
								await message.channel.send(content="/mc allowed in this channel",tts=False,embed=None)
							file = open("./command/ip.id", "w")
							for value in allowed:
								file.write(value+"\n")
							file.close()

	# A simple tic tac toe game
	if message.content.startswith(prefix+'ttt'):
		print("/ttt done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		if len(message.mentions) == 0:
			await message.channel.send("Please ping a player to play against.")
			return
		else:
			alone = False
			traitement = message.content.split(" ")
			for x in range(1,len(traitement)):
				if traitement[x].startswith("-"):
					if traitement[x].startswith("-self:"):
						if bool(traitement[x][7:].lower().capitalize()) in [True, False]:
							alone = bool(traitement[x][7:].lower().capitalize())
			if alone == False:
				player = [message.author,message.mentions[0]]
			else:
				player = [client.user,client.user]
			embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
			embed.add_field(name="Status",value="Waiting for "+str(player[1])+" to be ready (You have 5 minutes)",inline=False)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			host = await message.channel.send(content=None,tts=False,embed=embed)
			await host.add_reaction('✅')
			if player[1] != client.user:
				def check(reaction, user):
					return (user == player[1]) and (str(reaction.emoji) == '✅') and (reaction.message.id == host.id)
				try:
					reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
				except asyncio.TimeoutError:
					embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" VS "+str(player[1]), color=0xff0000)
					embed.add_field(name="Status",value="Battle Canceled",inline=False)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					await host.clear_reaction('✅')
					return		
			await host.clear_reaction('✅')
			turn = random.randint(0,1)
			grille = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
			hud = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:"]
			embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" :regional_indicator_o: VS :regional_indicator_x: "+str(player[1]), color=0xffff00)
			display = []
			for x in range(0,len(grille)):
				if grille[x] == -1:
					display.append(hud[x])
			embed.add_field(name="Grid",value=display[0]+display[1]+display[2]+"\n"+display[3]+display[4]+display[5]+"\n"+display[6]+display[7]+display[8])
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await host.edit(content=None,tts=False,embed=embed)
			# Jeu
			default = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮"]
			react = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮"]
			while True:
				action = ""
				embed.add_field(name="Current turn",value=str(player[turn]),inline=False)
				if player[turn] != client.user:
					if player[turn].dm_channel == None:
						await player[turn].create_dm()
					play = await player[turn].dm_channel.send(content="It's your turn to play! You have 5 minutes!", embed=embed)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					for x in react:
						await play.add_reaction(x)
					def checkPlay(reaction, user):
						nonlocal action
						nonlocal turn
						action = str(reaction.emoji)
						return (user == player[turn]) and (str(reaction.emoji) in react) and (reaction.message.id == play.id)
					try:
						reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=checkPlay)
					except asyncio.TimeoutError:
						embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" :regional_indicator_o: VS :regional_indicator_x: "+str(player[1]), color=0xff0000)
						embed.add_field(name="Status",value=str(player[turn])+" failed to play in time",inline=False)
						embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
						await host.edit(content=None,tts=False,embed=embed)
						return
				else:
					# IA
					possibiliter = [0,0,0,0,0,0,0,0,0]
					for x in range(0,9):
						temp = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
						for y in range(0,9):
							temp[y] = grille[y]
						if temp[x] != -1: # Check if we can play
							possibiliter[x] = -1000000
						else:
							# Check if we can win
							temp[x] = turn
							winner = -1
							if (((temp[0] == temp[1]) and (temp[1] == temp[2])) or ((temp[0] == temp[3]) and (temp[3] == temp[6])) or ((temp[0] == temp[4]) and (temp[4] == temp[8]))) and (temp[0] == temp[x]):
								winner = 0
							elif ((temp[3] == temp[4]) and (temp[4] == temp[5])) and (temp[3] == temp[x]):
								winner = 3
							elif (((temp[6] == temp[7]) and (temp[7] == temp[8])) or ((temp[6] == temp[4]) and (temp[4] == temp[2]))) and (temp[6] == temp[x]):
								winner = 6
							elif (temp[1] == temp[4]) and (temp[4] == temp[7]) and (temp[1] == temp[x]):
								winner = 1
							elif (temp[2] == temp[5]) and (temp[5] == temp[8]) and (temp[2] == temp[x]):
								winner = 2
							if winner != -1: #If we can, give it the highest priority because it can end the game
								possibiliter[x] = 1000000
							else:
								# Check if we can lose
								if turn == 1:
									temp[x] = 0
								else:
									temp[x] = 1
								winner = -1
								if (((temp[0] == temp[1]) and (temp[1] == temp[2])) or ((temp[0] == temp[3]) and (temp[3] == temp[6])) or ((temp[0] == temp[4]) and (temp[4] == temp[8]))) and (temp[0] == temp[x]):
									winner = 0
								elif ((temp[3] == temp[4]) and (temp[4] == temp[5])) and (temp[3] == temp[x]):
									winner = 3
								elif (((temp[6] == temp[7]) and (temp[7] == temp[8])) or ((temp[6] == temp[4]) and (temp[4] == temp[2]))) and (temp[6] == temp[x]):
									winner = 6
								elif (temp[1] == temp[4]) and (temp[4] == temp[7]) and (temp[1] == temp[x]):
									winner = 1
								elif (temp[2] == temp[5]) and (temp[5] == temp[8]) and (temp[2] == temp[x]):
									winner = 2
								if winner != -1: #If it can, give it the high priority because it can end the game
									possibiliter[x] = 100000
								else:
									# Check for the best attack place
									temp[x] = turn
									if x == 4:
										possibiliter[x] = 10000
									else:
										for offset in range(0,3): # We check every line
											if x in range(3*offset,3*(offset+1)):
												for y in range(3*offset,3*(offset+1)):
													if temp[y] == turn:
														possibiliter[x] = possibiliter[x] + 2
													elif temp[y] == -1:
														possibiliter[x] = possibiliter[x] + 1
													else:
														possibiliter[x] = possibiliter[x] - 2
										for offset in range(0,3): # We check every collumn
											if x in [(0+offset),(3+offset),(6+offset)]:
												for y in [(0+offset),(3+offset),(6+offset)]:
													if temp[y] == turn:
														possibiliter[x] = possibiliter[x] + 2
													elif temp[y] == -1:
														possibiliter[x] = possibiliter[x] + 1
													else:
														possibiliter[x] = possibiliter[x] - 2
										if x in [0,4,8]: #We check first diagonal
											for y in [0,4,8]:
												if temp[y] == turn:
													possibiliter[x] = possibiliter[x] + 2
												elif temp[y] == -1:
													possibiliter[x] = possibiliter[x] + 1
												else:
													possibiliter[x] = possibiliter[x] - 2
										if x in [2,4,6]: #We check second
											for y in [2,4,6]:
												if temp[y] == turn:
													possibiliter[x] = possibiliter[x] + 2
												elif temp[y] == -1:
													possibiliter[x] = possibiliter[x] + 1
												else:
													possibiliter[x] = possibiliter[x] - 2
					# Check which possibility is the highest
					highest = -10
					action = []
					for x in range(0,9):
						if possibiliter[x] > highest:
							highest = possibiliter[x]
					for x in range(0,9):
						if possibiliter[x] == highest:
							action.append(x)
					action = random.choice(action)
					if action != -1:
						action = default[action]
				for x in range(0,9):
					if action == default[x]:
						grille[x] = turn
				react.remove(action)
				winner = -1
				if (((grille[0] == grille[1]) and (grille[1] == grille[2])) or ((grille[0] == grille[3]) and (grille[3] == grille[6])) or ((grille[0] == grille[4]) and (grille[4] == grille[8]))) and (grille[0] != -1):
					winner = 0
				elif ((grille[3] == grille[4]) and (grille[4] == grille[5])) and (grille[3] != -1):
					winner = 3
				elif (((grille[6] == grille[7]) and (grille[7] == grille[8])) or ((grille[6] == grille[4]) and (grille[4] == grille[2]))) and (grille[6] != -1):
					winner = 6
				elif (grille[1] == grille[4]) and (grille[4] == grille[7]) and (grille[1] != -1):
					winner = 1
				elif (grille[2] == grille[5]) and (grille[5] == grille[8]) and (grille[2] != -1):
					winner = 2
				if winner != -1:
					embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" :regional_indicator_o: VS :regional_indicator_x: "+str(player[1]), color=0x00ff00)
					display = []
					for x in range(0,len(grille)):
						if grille[x] == -1:
							display.append(hud[x])
						elif grille[x] == 0:
							display.append(":regional_indicator_o:")
						else:
							display.append(":regional_indicator_x:")
					embed.add_field(name="Grid",value=display[0]+display[1]+display[2]+"\n"+display[3]+display[4]+display[5]+"\n"+display[6]+display[7]+display[8])
					embed.add_field(name="Winner", value=str(player[turn]))
					if player[0] != client.user:
						await player[0].dm_channel.send(content=None, embed=embed)
					if player[1] != client.user:
						await player[1].dm_channel.send(content=None, embed=embed)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					return
				elif -1 in grille:
					embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" :regional_indicator_o: VS :regional_indicator_x: "+str(player[1]), color=0xffff00)
					display = []
					for x in range(0,len(grille)):
						if grille[x] == -1:
							display.append(hud[x])
						elif grille[x] == 0:
							display.append(":regional_indicator_o:")
						else:
							display.append(":regional_indicator_x:")
					embed.add_field(name="Grid",value=display[0]+display[1]+display[2]+"\n"+display[3]+display[4]+display[5]+"\n"+display[6]+display[7]+display[8])
					if turn == 0:
						turn = 1
					else:
						turn = 0
				else:
					embed = discord.Embed(title="Tic-Tac-Toe", description=str(player[0])+" :regional_indicator_o: VS :regional_indicator_x: "+str(player[1]), color=0x00ffff)
					display = []
					for x in range(0,len(grille)):
						if grille[x] == -1:
							display.append(hud[x])
						elif grille[x] == 0:
							display.append(":regional_indicator_o:")
						else:
							display.append(":regional_indicator_x:")
					embed.add_field(name="Grid",value=display[0]+display[1]+display[2]+"\n"+display[3]+display[4]+display[5]+"\n"+display[6]+display[7]+display[8])
					embed.add_field(name="Winner", value="Nobody")
					if player[0] != client.user:
						await player[0].dm_channel.send(content=None, embed=embed)
					if player[1] != client.user:
						await player[1].dm_channel.send(content=None, embed=embed)
					embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
					await host.edit(content=None,tts=False,embed=embed)
					return

	# Gives info about a server
	if message.content.startswith(prefix+'server'):
		print("/server done by "+str(message.author)+"("+str(message.author.id)+") at "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		try:
			embed = discord.Embed(title="Info about "+str(message.channel.guild.name), description=None, color=message.author.color)
			embed.set_thumbnail(url=message.channel.guild.icon_url)
			embed.add_field(name="ID:", value=str(message.channel.guild.id), inline=False)
			embed.add_field(name="Owner:", value=str(message.channel.guild.owner)+" ("+str(message.channel.guild.owner.id)+")", inline=False)
			embed.add_field(name="Created:", value=str(message.channel.guild.created_at)[:-3], inline=False)
			embed.add_field(name="Members:", value=str(message.channel.guild.member_count))
			embed.add_field(name="Boost:", value=str(message.channel.guild.premium_subscription_count))
			if message.channel.guild.banner != None:
				embed.set_image(url=message.channel.guild.banner_url)
			embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
			await message.channel.send(content=None,tts=False,embed=embed)
		except AttributeError:
			await message.channel.send(content="You must be in a server to execute that command",tts=False,embed=None)
			return
		else:
			return

# A quick script to open the file having the bot token, get the token and launch the bot with the token
file = open("./settings/token.id", "r")
Token = file.readline()
file.close()
# print("Token: "+str(Token)) # Uncomment this line to see in the CMD what is your bot's current token
print("Discord Version is: "+str(discord.version_info.releaselevel)+" "+str(discord.__version__))
client.run(Token)