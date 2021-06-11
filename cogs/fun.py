import discord
from discord.ext import commands
import random
import aiohttp

snipe_message_author = {}
snipe_message_content = {}

class Fun(commands.Cog):
    '''Some commands to entertain you!'''

    def _init_(self, client):
        self.client = client
  
    @commands.command(description="Calculates the given expression")
    async def calc(self, ctx, *, expression):
        '''Calculates the given expression"'''
        if len(expression) > 10000000:
            await ctx.send("**Too big equation**")
        else:
            st = expression.replace("+", "%2B")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.mathjs.org/v4/?expr={st}"
                ) as response:
                    ex = await response.text()
                    if len(ex) > 10000000:
                        await ctx.send("Too big result")
                    else:

                        embed = discord.Embed(
                            timestamp=ctx.message.created_at,
                            title="Expression",
                            description=f"```{expression}```",
                            color=random.randint(0, 0xFFFFFF),
                        )
                        embed.add_field(
                            name=f"Result", value=f"```{ex}```", inline=False
                        )
                        embed.set_author(
                            name="Calculator",
                            icon_url="https://www.webretailer.com/wp-content/uploads/2018/10/Flat-calculator-representing-Amazon-FBA-calculators.png",
                        )
                        await ctx.send(embed=embed)

    @commands.command(name="catgirl")
    async def catgirl(self, ctx):
      '''Sends picture of a catgirl!'''
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://neko-love.xyz/api/v1/neko')
       cgjson = await request.json()
      embed = discord.Embed(title="Catgirl ;3 nya",color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=cgjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def catboy(self, ctx):
      '''Sends picture of a catboy!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://api.catboys.com/img')
        cbjson = await request.json()
      embed= discord.Embed(title="Catboy ;3 nya", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=cbjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def catto(self, ctx):
      '''Sends picture of a cat!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')
        catjson = await request.json()
      embed= discord.Embed(title="Cat! meow", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=catjson['link'])
      await ctx.send(embed=embed)

    @commands.command()
    async def doggo(self, ctx):
      '''Sends picture of a dog!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
      embed= discord.Embed(title="Dog! Woof Woof", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=dogjson['link'])
      await ctx.send(embed=embed)

    @commands.command()
    async def duck(self, msg):
     '''Sends pictures of a duck!'''
     async with aiohttp.ClientSession() as req:
      async with req.get('https://random-d.uk/api/v1/random') as duck:
        duck = await duck.json()
        return await msg.channel.send(duck['url'])

    @commands.command(pass_context=True)
    async def meme(self, ctx):
     '''Sends a random meme from Reddit'''
     embed = discord.Embed(title="Haha funni",color=random.randint(0, 0xFFFFFF) )
     async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def cock(self, ctx):
     '''Sends a random cock'''
     embed = discord.Embed(title="Cluck Cluck",color=random.randint(0, 0xFFFFFF) )
     async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/chickens.json') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, *, member):
      '''Hugs a person!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/hug')
        hugjson = await request.json()
        author_name = ctx.message.author.name
      embed= discord.Embed(title=f"{author_name} hugs {member}", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=hugjson['link'])
      await ctx.send(embed=embed)

    @commands.command()
    async def wink(self, ctx):
      '''Wink Wink ;)'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/wink')
        hugjson = await request.json()
      embed= discord.Embed(title=f"*Wink Wink*", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=hugjson['link'])
      await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, *, member):
      '''Pats a person!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/pat')
        patjson = await request.json()
        author_name = ctx.message.author.name
      embed= discord.Embed(title=f"{author_name} pats {member}", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=patjson['link'])
      await ctx.send(embed=embed)
  
    @commands.command()
    async def cry(self, ctx):
      '''For when you're sad'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://neko-love.xyz/api/v1/cry')
        hugjson = await request.json()
      embed= discord.Embed(title=f"*sobs*", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=hugjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, *, member):
      '''Kisses a person!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://neko-love.xyz/api/v1/kiss')
        patjson = await request.json()
        author_name = ctx.message.author.name
      embed= discord.Embed(title=f"{author_name} kisses {member}", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=patjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, *, member):
      '''Slaps a person!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://neko-love.xyz/api/v1/slap')
        patjson = await request.json()
        author_name = ctx.message.author.name
      embed= discord.Embed(title=f"{author_name} slaps {member}", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=patjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, *, member):
      '''Punch a person!'''
      async with aiohttp.ClientSession() as session:
        request = await session.get('https://neko-love.xyz/api/v1/punch')
        patjson = await request.json()
        author_name = ctx.message.author.name
      embed= discord.Embed(title=f"{author_name} punches {member}", color=random.randint(0, 0xFFFFFF))
      embed.set_image(url=patjson['url'])
      await ctx.send(embed=embed)

    @commands.command()
    async def sam(self, ctx):
     embed=discord.Embed(color=random.randint(0, 0xFFFFFF))
     embed.set_image(url="https://cdn.discordapp.com/attachments/747480159837487193/850528508396437564/E2t8l69XEAIh30E.png")
     await ctx.send(embed=embed)

    @commands.command(name= '8ball', aliases=['ball'])
    async def _8ball(self, ctx, *, question):
              '''See what the fates have in store for you'''
              responses = ['As I see it, yes.',
                          'Ask again later.',
                          'Better not tell you now.',
                          'Cannot predict now.',
                          'Concentrate and ask again.',
                          'Don’t count on it.',
                          'It is certain.',
                          'It is decidedly so.',
                          'Most likely.',
                          'My reply is no.',
                          'My sources say no.',
                          'Outlook not so good.',
                          'Outlook good.',
                          'Reply hazy, try again.',
                          'Signs point to yes.',
                          'Very doubtful.',
                          'Without a doubt.',
                          'Yes.',
                          'Yes – definitely.',
                          'You may rely on it.']
              a = (random.choice(responses))
              embed = discord.Embed(
                  description=(a),
                  colour=random.randint(0, 0xFFFFFF)
              )

              await ctx.send(embed=embed)

    @commands.command(name="dick", aliases=['pp'])
    async def dick(self, context, member: discord.Member = None):
        """
        Get the dick's length of a user or yourself.
        """
        if not member:
            member = context.author
        length = random.randrange(20)
        embed = discord.Embed(description=f"8{'=' * length}D", color=random.randint(0, 0xFFFFFF))
        embed.set_author(name=f"{member.display_name}'s dick", icon_url=member.avatar_url)
        await context.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))