# Mikobot 2.0 (re-write)
# Imports Discord.py
import discord 
# imports commands from discord.ext module 
from discord.ext import commands
# imports OS module
import os
# imports Flask modules that keep the bot alive
from keep_alive import keep_alive
# impots random module for 8ball command
import random 
# imports aiohttp for doggo and catto command
import aiohttp
#for dates
import datetime

# Bot prefix + client 
client = commands.Bot(command_prefix = ['miko ','m!','Miko '])

#removes on-board help command so we can put or own custom help command
 # client.remove_command("help")

# 'On Ready' command. Basically this confirms that the bot is active by leaving a message inside the console. 
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('the milk in my pfp is actually breast milk, #mommymilkers4life'))
  print('We have logged in as {0.user}'.format(client))

# Adds 2 numbers together 
@client.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

# Ping command
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! We are running at around {round(client.latency * 1000)} ms')

# userinfo command. Displays ID, name, account creation date, account join date, lists and displays roles, displays top role, and verifies if the user is a bot or not
@client.command()
async def userinfo(ctx, member: discord.Member = None):
  member = ctx.author if not member else member
  roles = [role for role in member.roles]
  
  embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
  embed.set_author(name=f"User Info - {member}")
  embed.set_thumbnail(url=member.avatr_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="ID:", value=member.id)
  embed.add_field(name='Name:', value=member.display_name)

  embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
  embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

  embed.add_field(name=f"Roles ({len(roles)})", value= " ".join([role.mention for role in roles]))
  embed.add_field(name="Top role:", value=member.top_role.mention)

  embed.add_field(name='Is this member a Bot?', value=member.bot)
    
#8ball command. Chooses from given responces when asked a question.
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = [
  discord.Embed(title='It is certain.'),
  discord.Embed(title='It is decidedly so.'),
  discord.Embed(title='Without a doubt.'),
  discord.Embed(title='Yes - definitely.'),
  discord.Embed(title='You may rely on it.'),
  discord.Embed(title='Most likely.'),
  discord.Embed(title='Outlook good.'),
  discord.Embed(title='Yes.'),
  discord.Embed(title='Signs point to yes.'),
  discord.Embed(title='Reply hazy, try again.'),
  discord.Embed(title='Ask again later.'),
  discord.Embed(title='Better not tell you now.'),
  discord.Embed(title='Cannot predict now.'),
  discord.Embed(title='Concentrate and ask again.'),
  discord.Embed(title="Don't count on it."),
  discord.Embed(title='My reply is no.'),
  discord.Embed(title='My sources say no.'),
  discord.Embed(title='Outlook not very good.'),
  discord.Embed(title='Very doubtful.')
    ]
  responses = random.choice(responses)
  await ctx.send(content=f'My Answer is: ' , embed=responses)

# Clear command. Removes a set amount of messages (set by the command executer)
#5 is the default ammount of messages cleared
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

#The below code displays if you have any errors publicly. This is useful if you don't want to display them in your output shell. Basically if you or the bot doesnt have enough perms, the bot will send an error message.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

#The below code bans a member.
@client.command()
@commands.has_permissions(ban_members = True)
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} is banned!")

#The below code unbans a member.
@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#The code below kicks a member
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = None):
  if not reason:
    await user.kick()
    await ctx.send(f"**{user}** has been kicked.")
  else:
    await user.kick(reason=reason)
    await ctx.send(f"**{user}** has been kicked for **{reason}**.")
    
# sends cat pic inside an embed
@client.command()
async def catto(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat') # Make a request
      catjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Catto! Meow", color=discord.Color.purple()) # Create embed
   embed.set_image(url=catjson['link']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed

# sends dog pic inside an embed
@client.command()
async def doggo(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') # Make a request
      dogjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Doggo! Woof Woof", color=discord.Color.purple()) # Create embed
   embed.set_image(url=dogjson['link']) # Set the embed image to the value of the 'link' key
   await ctx.send(embed=embed) # Send the embed

#server info
@client.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Example", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")

# keeps the bot alive, see more at ./keep_alive.py
keep_alive()
client.run(os.getenv('TOKEN'))