import discord
from discord.ext import commands
import random
import datetime
import json
bot = commands.Bot

def register(file, guild):
    with open(file, 'r+') as f:
        data = json.load(f)
    if str(guild.id) not in list(data):
        data[str(guild.id)] = {
            "AFK": {}
        }
        with open(file, 'w') as f:
            json.dump(data, f, indent = 4)

class General(commands.Cog, name="General"):
    """Basic commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bi", "about"])
    async def botinfo(self, ctx):
      embed = discord.Embed(timestamp=ctx.message.created_at, title="About me | Info", color=random.randint(0, 0xFFFFFF))
      embed.set_thumbnail(url=ctx.bot.user.avatar_url)
      embed.add_field(name="My Prefixes are:", value=f"`m!, miko`")
      embed.add_field(name="My Support Server", value="[Join My Server](https://discord.gg/CTfD3zvSCg)")
      embed.add_field(name="Add Me",value="[Click Here to Add Me](https://discord.com/api/oauth2/authorize?client_id=843097789831184394&permissions=8&scope=bot)")
      embed.add_field(name="Github",value="[Checkout my Github repo!](https://github.com/MikoTatsu/MikoBot)")
      embed.add_field(name="Made with Love By", value="Miko!#8008")
      embed.set_footer(text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
      await ctx.send(embed=embed)
      
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket latency."""
        embed=discord.Embed(title="Miko Bot's latency!",description=f"Pong! I'm running at about {round(self.bot.latency * 1000)} ms", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title=f"{poll_title}", color=random.randint(0, 0xFFFFFF)    
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")


    @commands.command(aliases=["ri","role"], no_pm=True)
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        '''Shows information about a role'''
        guild = ctx.guild

        since_created = (ctx.message.created_at - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{} ({} days ago!)".format(role_created, since_created)
        members = ''
        i = 0
        for user in role.members:
            members += f'{user.name}, '
            i+=1
            if i > 30:
                break

        if str(role.colour) == "#000000":
            colour = "default"
            color = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = str(role.colour).upper()
            color = role.colour

        em = discord.Embed(colour=color)
        em.set_author(name=role.name)
        em.add_field(name="Users", value=len(role.members))
        em.add_field(name="Mentionable", value=role.mentionable)
        em.add_field(name="Hoist", value=role.hoist)
        em.add_field(name="Position", value=role.position)
        em.add_field(name="Managed", value=role.managed)
        em.add_field(name="Colour", value=colour)
        em.add_field(name='Creation Date', value=created_on)
        em.add_field(name='Members', value=members[:-2], inline=False)
        em.set_footer(text=f'Role ID: {role.id}')

        await ctx.send(embed=em)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
      member = ctx.author if not member else member
      roles = [role for role in member.roles]

      embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
      embed.set_author(name=f"User Info - {member}")
      embed.set_thumbnail(url=member.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

      embed.add_field(name="ID:", value=member.id)
      embed.add_field(name='Name:', value=member.display_name)
      embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I: %M %p UTC"))
      embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I: %M %p UTC"))
      embed.add_field(name=f"Roles ({len(roles)})", value = " ".join([roles.mention for roles in roles]))
      embed.add_field(name="Top role:", value=member.top_role.mention)
    
      await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
      embed = discord.Embed(title=f"{ctx.guild.name}", timestamp=datetime.datetime.utcnow(), color=random.randint(0, 0xFFFFFF))
      embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
      embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
      embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
      embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
      embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
      embed.add_field(name="Bot Count", value= sum(1 for member in ctx.guild.members if member.bot))
      embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

      await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def dm(self, ctx, user: discord.User, *, message=None):
      '''Dms the pinged user with a custom message'''
      message = message or "This message is sent via DM."
      await ctx.message.delete()
      await user.send(message)

    @commands.command(aliases=['echo', 'repeat'])
    async def say(self, ctx, *, desc):
      await ctx.message.delete()
      embed = discord.Embed(description=desc, color=random.randint(0, 0xFFFFFF))
      await ctx.send(embed=embed)

    @commands.command(description="Sends your avatar pic or of mentioned user / id", aliases=['avatar'])
    async def av(self, ctx, member: discord.Member = None):
      '''Sends your avatar pic or of mentioned user / id'''
      if member is None:
          member = ctx.author
          a = member.avatar_url
          await ctx.send(a)
      else:
          a = member.avatar_url

          await ctx.send(a)

    @commands.command(aliases=['afk', 'Afk', 'aFk', 'afK','AFk', 'aFK', 'AfK'])
    async def AFK(self, ctx, *, reason=None):
        if reason == None:
            reason2 = 'I set your AFK'
            reason = ''
        else:
            reason2 = f'I set your AFK, status: {reason}'
        with open("enabled.json", "r") as f:
            data = json.load(f)
        print(list(data[str(ctx.guild.id)]['AFK']))
        if str(ctx.author.id) in list(data[str(ctx.guild.id)]['AFK']):
            await ctx.channel.send('You\'re a little to quick here')
            return

        
        data[str(ctx.guild.id)]['AFK'][str(ctx.author.id)] = reason
        await ctx.channel.send(f'{ctx.author.mention} {reason2}')
        

        with open("enabled.json", "w") as f:
            json.dump(data,f, indent = 4)
        try:
            await ctx.author.edit(nick='[AFK]'+ctx.author.name)
        except:
            pass
    @commands.Cog.listener()
    async def on_message(self, message):
        
        register('enabled.json', message.guild)
        if message.content.startswith('-'): 
            return
        with open("enabled.json", "r") as f:
            data = json.load(f)
        
        if str(message.author.id) in list(data[str(message.guild.id)]['AFK']):
            data[str(message.guild.id)]["AFK"].pop(str(message.author.id))
            with open("enabled.json", "w") as f:
                json.dump(data, f, indent=4)
            await message.channel.send(f'Welcome Back, I removed you AFK!')
        
        for i in message.mentions:
            if str(i.id) in list(data[str(message.guild.id)]['AFK']):
                if data[str(message.guild.id)]['AFK'][str(i.id)] != '':
                    reason = 'Reason: ' + data[str(message.guild.id)]['AFK'][str(i.id)]
                else:
                    reason = ''
                await message.channel.send(f'**`{i.name}`** is AFK. {reason}')
                break
        
    @commands.command(description="Adds the mentioned to role to mentioned/id memebr")
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, rolename: discord.Role):
        '''Adds the mentioned to role to mentioned/id memebr'''
        guild = ctx.guild
        if guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif rolename in ctx.guild.roles:
            await member.add_roles(rolename)
            embed = discord.Embed(
                title="Add Role",
                description=f"Added {rolename} role to {member.name}",
                color=random.randint(0, 0xFFFFFF),
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Error", description="Role not found", color=random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)

    @commands.command(description="Removed the mentioned role from mentioned user/id", aliases=['remrole'])
    @commands.has_permissions(manage_roles=True)
    async def unrole(self, ctx, member: discord.Member, rolename: discord.Role):
        '''Removed the mentioned role from mentioned user/id'''
        guild = ctx.guild
        if guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif rolename in ctx.guild.roles:

            await member.remove_roles(rolename)
            embed = discord.Embed(
                title="Remove role",
                description=f"Removed {rolename} role from {member.name}",
                color=random.randint(0, 0xFFFFFF),
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Error", description="Role not found",color=random.randint(0, 0xFFFFFF)
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """ Nicknames a user from the current server. """
        try:
            await member.edit(nick=name, reason=("Changed by command"))
            message = f"Changed **{member.name}'s** nickname to **{name}**"
            if name is None:
                message = f"Reset **{member.name}'s** nickname"
            await ctx.send(message)
        except Exception as e:
            await ctx.send(e)

# test
def setup(bot):
    bot.add_cog(General(bot))
    