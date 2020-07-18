import discord
# Discord API Reference: https://discordpy.readthedocs.io/en/v1.3.4/api.html
import datetime
import asyncio

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
				embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xff0000)
				embed.add_field(name="Status",value="Waiting for "+str(message.mentions[0])+" to be ready (You have 5 minutes)",inline=False)
				host = await message.channel.send(content=None,tts=False,embed=embed)
				await host.add_reaction('✅')
				def check(reaction, user):
					return (user == message.mentions[0]) and (str(reaction.emoji) == '✅') and (reaction.message.id == host.id)
				try:
					reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
				except asyncio.TimeoutError:
					embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xff0000)
					embed.add_field(name="Status",value="Battle Canceled",inline=False)
					await host.edit(content=None,tts=False,embed=embed)
					await host.clear_reaction('✅')
				else:
					await host.clear_reaction('✅')
					actionA = ""
					actionB = ""
					embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xffff00)
					embed.add_field(name="Status",value=str(message.author)+" is playing",inline=False)
					await host.edit(content=None,tts=False,embed=embed)
					if message.author.dm_channel == None:
						await message.author.create_dm()
					playerA = await message.author.dm_channel.send(content="It's your turn to play! You have 5 minutes!")
					scheme = ['✊','🖐','✌']
					for x in scheme:
						await playerA.add_reaction(x)
					def checkA(reaction, user):
						nonlocal actionA
						actionA = str(reaction.emoji)
						return (user == message.author) and (str(reaction.emoji) in scheme) and (reaction.message.id == playerA.id)
					try:
						reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=checkA)
					except asyncio.TimeoutError:
						embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xff0000)
						embed.add_field(name="Status",value=str(message.author)+" failed to play in time",inline=False)
						await host.edit(content=None,tts=False,embed=embed)
					else:
						embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xffff00)
						embed.add_field(name="Status",value=str(message.mentions[0])+" is playing",inline=False)
						await host.edit(content=None,tts=False,embed=embed)
						if message.mentions[0].dm_channel == None:
							await message.mentions[0].create_dm()
						playerB = await message.mentions[0].dm_channel.send(content="It's your turn to play! You have 5 minutes!")
						for x in scheme:
							await playerB.add_reaction(x)
						def checkB(reaction, user):
							nonlocal actionB
							actionB = str(reaction.emoji)
							return (user == message.mentions[0]) and (str(reaction.emoji) in scheme) and (reaction.message.id == playerB.id)
						try:
							reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=checkB)
						except asyncio.TimeoutError:
							embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xff0000)
							embed.add_field(name="Status",value=str(message.mentions[0])+" failed to play in time",inline=False)
							await host.edit(content=None,tts=False,embed=embed)
						else:
							status = ""
							if actionA == actionB:
								embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0xffa500)
								status = "Tie"
							elif (actionA == '🖐' and actionB == '✊') or (actionA == '✊' and actionB == '✌') or (actionA == '✌' and actionB == '🖐'):
								embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0x00ff00)
								status = str(message.author)+" won!"
							else:
								embed = discord.Embed(title="Rock Paper Scissors", description=str(message.author)+" VS "+str(message.mentions[0]), color=0x00ff00)
								status = str(message.mentions[0])+" won!"
							embed.add_field(name="Status",value=status,inline=False)
							embed.add_field(name="Playback",value=actionA+" VS "+actionB,inline=False)
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
			embed.add_field(name="Last Update", value="18/07/2020 - 14:30", inline=False)
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

# A quick script to open the file having the bot token, get the token and launch the bot with the token
file = open("./settings/token.id", "r")
Token = file.readline()
file.close()
# print("Token: "+str(Token)) # Uncomment this line to see in the CMD what is your bot's current token
print("Discord Version is: "+str(discord.version_info.releaselevel)+" "+str(discord.__version__))
client.run(Token)