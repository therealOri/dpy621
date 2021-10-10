# Code made by Ori#6338 | <- DO NOT REMOVE
import colorama
from colorama import Fore
import discord
from discord.ext import commands
import datetime
import aiohttp
import random
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
login = os.getenv("login")
bot_token = os.getenv('bot_token')

botver = "MyBot v0.0.1"

intents = discord.Intents.all()
BOT_Prefix=("!")
bot = commands.Bot(command_prefix=BOT_Prefix, intents=intents)

# Load .py files in folder called "cogs".
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(Fore.GREEN + f"Loaded {filename[:-3]}")
        
        
@bot.event
async def on_ready():
    print(Fore.WHITE + "[" + Fore.GREEN + '+' + Fore.WHITE + "]" + Fore.GREEN + f" connection established and logged in as: {bot.user.name} with ID: {bot.user.id}")


@bot.command(aliases=["e6"])
@commands.is_nsfw()
async def e621(ctx, *, args):
    await ctx.message.delete()
    loading = await ctx.send(f' ⌛ Looking for an image on e621 with tags **`{args}`**. ⌛')

    # Blacklisted words that can not be used.
    # May change in the future. Be my guest for how you want to change how it handles "tags" you shouldn't use.
    blist = ['cub', 'loli', 'shota', 'young', 'underage', 'blood', 'gore', 'death', 'dying', 'necrophilia']

    for bad_word in blist:
        if bad_word in args.lower():
            embed1 = discord.Embed(title=" 🚨 **Warning!** 🚨", description=f'Search Argument contains a blacklisted word. **`{bad_word}`** is a blacklisted word.', colour=0xff0000, timestamp=datetime.datetime.utcnow())
            embed1.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
            return await loading.edit(content='', embed=embed1)

    e621_agent = {
        'User-Agent': 'MyProject v0.0.1 (by UserName)',
        'login': login,
        'api_key': api_key
    }

    # e6_request = r.get(f'https://e621.net/posts.json?tags={args}&limit=100', headers=e621_agent)
    async with aiohttp.ClientSession(headers=e621_agent, auth=aiohttp.BasicAuth(login, api_key)) as session:
        async with session.get(f'https://e621.net/posts.json?tags={args}&limit=100') as e6_request:
            if not 200 <= e6_request.status < 300:
                net_embed = discord.Embed(title=" ⚠️ **Error** ⚠️ ", description=f"Network error. | Bad Request.\n Error code: `**{e6_request.status}**`", colour=0xff0000, timestamp=datetime.datetime.utcnow())
                net_embed.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                return await loading.edit(content="", embed=net_embed)
            json = await e6_request.json()

    try:
        data = json['posts']
        post = random.choice(data)
        score = str(post['score']['total'])
        post_id = str(post['id'])
        image = post['file']['url']

    except IndexError as e:
        embed_err = discord.Embed(title=" ⚠️ **Error!** ⚠️", description=f'Oof, Looks like there is nothing to find for `{args}`.\nError: {e}', colour=0xff0000, timestamp=datetime.datetime.utcnow())
        embed_err.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        return await loading.edit(embed=embed_err)

    file_ext = ["webm", "mp4", "gif", "swf"]
    if image.split('.')[-1] in file_ext:
        embed2 = discord.Embed(title="UwU | Webm, Mp4, Gif, or Swf format has been detected in post!", description=f" 🔞 e621 image found for **`{args}`** 🔞\n\n ⬆️ **Score:** {score}\n\n:link: **Post URL:** <https://e621.net/posts/{post_id}>\n\n:link: **Video URL:** {image}", colour=discord.Color.random(), timestamp=datetime.datetime.utcnow()) # TODO cool hyperlink thing
        embed2.set_image(url=image)
        embed2.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        return await loading.edit(content='', embed=embed2)

    embed3 = discord.Embed(title="UwU", description=f"🔞 e621 image for **`{args}`** 🔞 \n\n_ _ \n ⬆️ **Score:** {score}\n\n:link: **[Post URL](https://e621.net/posts/{post_id})**", colour=discord.Color.random())
    embed3.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
    embed3.set_image(url=image)
    await loading.edit(content='', embed=embed3)


@e621.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
        embed = discord.Embed(title="Error!", description="The channel this command was ran is was not a nsfw channel.\nPlease make sure to use this command in nsfw channels only.", color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        await ctx.send(embed=embed)
    else:
        raise error


bot.run(bot_token)
