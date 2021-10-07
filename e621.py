# Code made by Ori#6338 | <- DO NOT REMOVE
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import *
import json
import requests as r
import random
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
login = os.getenv("login")

botver = "MyBot v0.0.1"

@client.command(aliases=["e6"])
@commands.is_nsfw()
async def e621(ctx, *, args):
    await ctx.message.delete()
    loading = await ctx.send(f' ⌛ Looking for an image on e621 with tags **`{args}`**. ⌛')

    e621_agent = {
    'User-Agent': 'MyProject v0.0.1 (by UserName)',
    'login': login,
    'api_key': api_key
    }

    # Blacklisted words that can not be used.
    blist = ['cub', 'loli', 'shota', 'young', 'underage', 'blood', 'gore', 'death', 'dying', 'necrophilia'] # May change in the future. Be my guest for how you want to change how it handles "tags" you shouldn't use.
    
    for bad_word in blist:
            if bad_word in args.lower():
                embed1 = discord.Embed(title=" 🚨 **Error!** 🚨", description=f'Search Argument contains a blacklisted word. **`{bad_word}`** is a blacklisted word.', colour=0xff0000, timestamp=datetime.datetime.utcnow())
                embed1.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                await loading.edit(content='', embed=embed1)
                break

    if not bad_word in args.lower():
            e6_request = r.get(f'https://e621.net/posts.json?tags={args}&limit=100', headers=e621_agent).json()

            try:
                data = e6_request['posts']
                post = random.choice(data)
                score = str(post['score']['total'])
                post_id = str(post['id'])
                image = post['file']['url']

                file_ext = [".webm", ".mp4", ".gif", ".swf"]
                for x in file_ext:
                        print(x)
                        if image.endswith(x):
                            embed2 = discord.Embed(title="UwU | Webm, Mp4, Gif, or Swf format has been detected in post!", description=f" 🔞 e621 image found for **`{args}`** 🔞\n\n ⬆️ **Score:** {score}\n\n:link: **Post URL:** <https://e621.net/posts/{post_id}>\n\n:link: **Video URL:** {image}", colour=discord.Color.random(), timestamp=datetime.datetime.utcnow())
                            embed2.set_image(url=image)
                            embed2.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                            await loading.edit(content='', embed=embed2)
                            break
                        
                if not image.endswith(x):
                            embed3 = discord.Embed(title="UwU", description=f"🔞 e621 image for **`{args}`** 🔞 \n\n_ _ \n ⬆️ **Score:** {score}\n\n:link: **[Post URL](https://e621.net/posts/{post_id})**", colour=discord.Color.random())
                            embed3.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                            embed3.set_image(url=image)
                            await loading.edit(content='', embed=embed3)
                            

            
            except IndexError as e:
                embed_err = discord.Embed(title=" ⚠️ **Error!** ⚠️", description=f'Oof, Looks like there is nothing to find for `{args}`.\nError: {e}', colour=0xff0000, timestamp=datetime.datetime.utcnow())
                embed_err.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                await ctx.send(embed=embed_err)

@e621.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
        embed = discord.Embed(title="Error!", description="The channel this command was ran is was not a nsfw channel. Please make sure to use this command in nsfw channels only.", color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        await ctx.send(embed=embed)
