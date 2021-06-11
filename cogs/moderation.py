import asyncio
import discord
from discord.ext import commands
import aiofiles
import random
bot = commands.Bot
bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}


class Mod(commands.Cog):
    """Commands to help with moderation!"""
    def __init__(self, client):
        self.client = client

    @commands.command(description="Bans a member")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx, member: discord.Member, *, reason=None, delete_message_days=7
    ):
        """Bans a member."""
        guild = ctx.guild
        if member == self.client.user:

            await ctx.send("**Haha, i am immortal**")

        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot ban a bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot ban yourself**")
        else:

            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Ban",
                description=f"{member.name} has been banned by {ctx.author.name}",
                color=random.randint(0, 0xFFFFFF),
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['hban'])
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, ID:int):
      """Bans a member that is not inside the server."""
      await ctx.guild.ban(discord.Object(id=ID))
      embed = discord.Embed(title='Ban', description=f"<@{ID}> has been banned by {ctx.author.name}", color=random.randint(0, 0xFFFFFF))
      await ctx.send(embed=embed)

    @commands.command( description="Unbans a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        """Unbans a member."""
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="Unban",
            description=f"{id} has been unbanned by {ctx.author.name}",
            color=random.randint(0, 0xFFFFFF),
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def bans(self, ctx):
        '''Lists all banned members in the server.'''
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Reason:\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('There are no banned members!')

    @commands.command(aliases=["del", "p", "purge"])
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount=4):
        """Deletes the given amount of messages."""
        if amount > 200:
            await ctx.send("**Currently due to bot hosting we support only 200 limit**")
        else:
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"**Purged {amount} messages**")
            await asyncio.sleep(2)
            await msg.delete()

    @commands.command(description="Kicks a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member"""
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot kick me dumbass**")
        elif member == ctx.author:
            await ctx.send("**You cannot kick yourself dumb bitch**")
        else:

            if member.top_role < ctx.author.top_role:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="Kick",
                    description=f"{member.name} has been kicked by {ctx.author.name}",
                    color=random.randint(0, 0xFFFFFF),
                )
                await ctx.send(embed=embed)

    @commands.command(
        description="Softbans a member ( Unban after ban to clear chat , to clear chat )"
    )
    @commands.has_permissions(kick_members=True, ban_members = True)
    async def softban(self, ctx, member: discord.Member):
        """Bans then unbans a member."""
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot ban me dumbass**")
        elif member == ctx.author:
            await ctx.send("**You cannot ban yourself dumb bitch**")
        else:

            await member.ban(reason=None, delete_message_days=7)

            await ctx.guild.unban(member, reason=None)

            embed = discord.Embed(
                title="SoftBan",
                description=f"{member.name} has been softbanned by {ctx.author.name}",
                color=random.randint(0, 0xFFFFFF),
            )
            await ctx.send(embed=embed)

    @commands.command(description="Mutes a member")
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, user: discord.Member, reason=None):
        '''Mutes a member'''
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if user == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < user.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif user.bot:
            await ctx.send("**You cannot mute bot**")
        elif user == ctx.author:
            await ctx.send("**You cannot mute yourself**")
        else:
            if not role:
                try:
                    muted = await ctx.guild.create_role(
                        name="Muted", reason="To use for muting"
                    )
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(
                            muted,
                            send_messages=False,
                            read_message_history=False,
                            view_channels=True,
                            read_messages=False,
                        )
                except discord.Forbidden:
                    return await ctx.send(
                        "I have no permissions to make a muted role"
                    )  # self-explainatory
                await user.add_roles(muted)
                embed = discord.Embed(
                    title="Muted",
                    description=f"{user.name} has been muted",
                    color=random.randint(0, 0xFFFFFF),
                )
                await ctx.send(embed=embed)

            elif role in user.roles:
                embed = discord.Embed(
                    title="Invalid usage",
                    description="User is already muted",
                    color=random.randint(0, 0xFFFFFF),
                )
                await ctx.send(embed=embed)
            else:
                await user.add_roles(role)
                embed = discord.Embed(
                    title="Muted",
                    description=f"{user.name} has been muted",
                    color=random.randint(0, 0xFFFFFF),
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True, manage_messages = True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmutes a member'''
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if guild.me.top_role < user.top_role:
            await ctx.send("**Member is higher than me in the role hierarchy**")
        elif role not in user.roles:
            embed = discord.Embed(
                title="Invalid usage",
                description="User is already unmuted",
                color=random.randint(0, 0xFFFFFF),
            )
            await ctx.send(embed=embed)

        else:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
            embed = discord.Embed(
                title="Unmuted",
                description=f"{user.name} has been unmuted",
                color=random.randint(0, 0xFFFFFF),
            )
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
      bot.warnings[guild.id] = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self,ctx, member: discord.Member=None, *, reason=None):
       if member is None:
         return await ctx.send("Did you specify a user? if so, then that person probably isn't in the server.")
       
       if reason is None:
         return await ctx.send("Please provide a warning for the user.")
        
       try:
         first_warning = False
         bot.warnings[ctx.guild.id][member.id][0] += 1
         bot.warnings[ctx.guild.id][member.id][1].append[(ctx.author.id, reason)]

       except KeyError:
         first_warning = True
         bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
        
       count = bot.warnings[ctx.guild.id][member.id][0]

       async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
         await file.write(f"{member.id} {ctx.author.id} {reason}\n")

       await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member=None):
       if member is None:
         return await ctx.send("Did you specify a user? if so, then that person probably isn't in the server.")

       embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
       try:
         i = 1
         for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

         await ctx.send(embed=embed)

       except KeyError:
         await ctx.send("This user has no warnings.") 


    @commands.command(description="Locks the channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        '''Locks the channel'''
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            embed = discord.Embed(
                title="Invalid usage",
                description="This channel is already locked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)
        else:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="Channel Locked",
                description="This channel is now Locked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)

    @commands.command(description="Unlocks the locked channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        '''Unlocks the locked channel'''
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
            embed = discord.Embed(
                title="Invalid usage",
                description="This channel is already unlocked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)
        else:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="Channel Unlocked",
                description="This channel is now unlocked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Mod(client))