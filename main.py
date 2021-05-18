## Mikobot 2.0 (re-write)
# Imports 
import discord 
from discord.ext import commands
import os
#from keep_alive import keep_alive
import random 
import aiohttp
import datetime
import aiofiles

#intents
intents = discord.Intents.default()
intents.members = True

# Bot prefix + client 
client = commands.Bot(command_prefix = ['miko ','m!','Miko '], intents=intents, help_command=None)
bot = client
bot.sniped_messages = {}

# 'On Ready' command. Basically this confirms that the bot is active by leaving a message inside the console. 
bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}
@client.event
async def on_ready():
  for guild in client.guilds: # creates a .txt file which stores all the ID's of the warned person, the person who warned, and warn reason
        client.warnings[guild.id] = {}
        async with aiofiles.open(f"{guild.id}.txt", mode="a"):
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 
  await client.change_presence(status=discord.Status.online, activity=discord.Game('#mommymilkers4life'))
  print('We have logged in as {0.user}'.format(client))

# Adds 2 numbers together 
@client.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

# Subtracts 2 numbers together 
@client.command()
async def sub(ctx, left: int, right: int):
    await ctx.send(left - right)

# Multiplies 2 numbers together 
@client.command()
async def multiply(ctx, left: int, right: int):
    await ctx.send(left * right)

# divides 2 numbers together 
@client.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)

# Ping command
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! We are running at around {round(client.latency * 1000)} ms')

# dm command
@bot.command()
@commands.has_permissions(administrator = True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)

#change nickname
@client.command(pass_context=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

#snipe command
@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

# userinfo command. Displays ID, name, account creation date, account join date, lists and displays roles, displays top role, and verifies if the user is a bot or not
@client.command()
async def userinfo(ctx, member: discord.Member = None):
  member = ctx.author if not member else member
  roles = [role for role in member.roles]
  
  embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
  embed.set_author(name=f"User Info - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="ID:", value=member.id)
  embed.add_field(name='Name:', value=member.display_name)

  embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
  embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

  embed.add_field(name=f"Roles ({len(roles)})", value= " ".join([role.mention for role in roles]))
  embed.add_field(name="Top role:", value=member.top_role.mention)

  await ctx.send(embed=embed)
    
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
  await ctx.send(embed=responses)

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
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned!")

#The below code unbans a member.
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member_id: int):
		await ctx.message.delete()
		try:
			await ctx.guild.unban(discord.Object(id=member_id))
			await ctx.send(f"<@{member_id}> was Unbanned!")
		except Exception as e:
			await ctx.send(f'```{type(e).__name__} - {e}```')
    
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

# sends duck pic
@client.command()
async def duck(msg):
 async with aiohttp.ClientSession() as req:
    async with req.get('https://random-d.uk/api/v1/random') as duck:
        duck = await duck.json()
        return await msg.channel.send(duck['url'])

@client.command()
async def catboy(ctx):
   async with aiohttp.ClientSession() as session:
      request3 = await session.get('https://api.catboys.com/img') # Make a request
      cbjson = await request3.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Catboy ;) nya", color=discord.Color.purple()) # Create embed
   embed.set_image(url=cbjson['url']) # Set the embed image to the value of the 'url' key
   await ctx.send(embed=embed) # Send the embed

@client.command()
async def catgirl(ctx):
   async with aiohttp.ClientSession() as session:
      request4 = await session.get('https://neko-love.xyz/api/v1/neko') # Make a request
      cgjson = await request4.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Catgirl ;) nya", color=discord.Color.purple()) # Create embed
   embed.set_image(url=cgjson['url']) # Set the embed image to the value of the 'url' key
   await ctx.send(embed=embed) # Send the embed

# sends random meme inside an embed
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="Haha funni",color=discord.Color.purple() )

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
        
#server info
@client.command()
async def serverinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    await ctx.send(embed=embed)

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

#warn command, uses libraries 
@client.event
async def on_guild_join(guild):
    client.warnings[guild.id] = {}

@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    try:
        first_warning = False
        client.warnings[ctx.guild.id][member.id][0] += 1
        client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = client.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

@client.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in client.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")

#mute command
@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")
#unmute command
@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

# cogs
# load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
# unload cogs
@client.command()
async def unload(ctx, extension):
    client.unload_extention(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# keeps the bot alive, see more at ./keep_alive.py [replit.com only!]
 #keep_alive()
# Token Hidden  
client.run(os.getenv('TOKEN'))
