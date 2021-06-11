# Mikobot 2.0 (re-write)
# Imports
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import aiofiles

#intents
intents = discord.Intents.default()
intents.members = True

# Bot prefix + client
client = commands.Bot(command_prefix=['miko ', 'm!', 'Miko '],
                      intents=intents,
                      help_command=None)
bot = client
bot.sniped_messages = {}


# 'On Ready' command. Basically this confirms that the bot is active by leaving a message inside the console.
@client.event
async def on_ready():
	for guild in bot.guilds:
		bot.warnings[guild.id] = {}

		async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
			pass

		async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
			lines = await file.readlines()

			for line in lines:
				data = line.split(" ")
				member_id = int(data[0])
				admin_id = int(data[1])
				reason = " ".join(data[2:]).strip("\n")

				try:
					bot.warnings[guild.id][member_id][0] += 1
					bot.warnings[guild.id][member_id][1].append(
					    (admin_id, reason))

				except KeyError:
					bot.warnings[guild.id][member_id] = [
					    1, [(admin_id, reason)]
					]

	await client.change_presence(status=discord.Status.online,
	                             activity=discord.Activity(
	                                 type=discord.ActivityType.watching,
	                                 name="it jiggle"))
	print('We have logged in as {0.user}'.format(client))


#The below code displays if you have any errors publicly. This is useful if you don't want to display them in your output shell. Basically if you or the bot doesnt have enough perms, the bot will send an error message.
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please pass in all requirements.')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("You dont have enough permissions to use this command. "
		               )


# cogs
# load cogs
@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


# unload cogs
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extention(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

# keeps the bot alive, see more at ./keep_alive.py [replit.com only!]
#keep_alive()
# Token Hidden
client.run(os.getenv('TOKEN'))

