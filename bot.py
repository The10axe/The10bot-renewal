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
			embed.add_field(name="/sncf", value="The satanic invocation of a french train")
			embed.add_field(name="/wtn [-min:<value>] [-max:<value>] [-force:<true|false>] [-ttj:<value>] [-ttp:<value>] [user]", value="Begin a \"What's the number\" game, forcing will put all non ready player AFK, ttj is Time To Join, ttp is Time To Play")
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
			embed.add_field(name="Current version", value="Stable")
			embed.add_field(name="Last Update", value="26/07/2020 - 11:30", inline=False)
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
	
	# A game about encrypted messages
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
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binary[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
			await message.channel.send(content=None,tts=False,embed=embed)
			embed = discord.Embed(title="Converting table for "+str(message.author), description="Part 2", color=message.author.color)
			for x in range(24,len(lettre)):
				embed.add_field(name=("`"+lettre[x]+"`"),value=("`"+str(binary[x])+" | "+str(octal[x])+" | "+str(hexa[x])+"`\n`"+str(morse[x])+"`"))
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
				await host.edit(content=None,tts=False,embed=embed)
				await host.add_reaction('👏')
				return

# A quick script to open the file having the bot token, get the token and launch the bot with the token
file = open("./settings/token.id", "r")
Token = file.readline()
file.close()
# print("Token: "+str(Token)) # Uncomment this line to see in the CMD what is your bot's current token
print("Discord Version is: "+str(discord.version_info.releaselevel)+" "+str(discord.__version__))
client.run(Token)