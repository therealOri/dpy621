# Code made by Ori#6338 | <- DO NOT REMOVE

# Same command but for slash commands in a cog. I like to put my slash commands in a seprate file/cog.
import discord
from discord.ext import commands
from discord.ext.commands import *
from discord_slash import SlashCommand, SlashContext, cog_ext
import aiohttp
from dotenv import load_dotenv
import os
import random
import json
import datetime
import sqlite3

load_dotenv()
api_key = os.getenv("api_key")
login = os.getenv("login")

botver = "MyBot v0.0.1"
guild_ids=[GUILD_ID_HERE]

database = sqlite3.connect('tag_blacklist.db')
c = database.cursor()

class e621Slash(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot


    @cog_ext.cog_slash(name="e6", description="A nsfw command to get all the yiff using the e621 api. | Example: /e6 <tag tag tag_tag>", guild_ids=guild_ids)
    @commands.is_nsfw()
    async def e6(self, ctx: SlashContext, arg: str):
        loading = await ctx.send(f' ⌛ Looking for an image on e621 with tags **`{arg}`**. ⌛')

        # Blacklisted words that can not be used. | This is to make sure users can't use blacklisted words in their search.
        c.execute('SELECT tag_names FROM tags')
        ldb = c.fetchall()
        ldb = str(ldb).replace("(", "").replace(",)", "").replace("'", "")
        blist = ldb.strip('][').split(', ')

        for bad_word in blist:
            if bad_word in arg.lower():
                embed1 = discord.Embed(title=" 🚨 **Warning!** 🚨", description=f'Search Argument contains a blacklisted word. **`{bad_word}`** is a blacklisted word.', colour=0xff0000, timestamp=datetime.datetime.utcnow())
                embed1.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
                return await loading.edit(content='', embed=embed1)

        e621_agent = {
            'User-Agent': 'MyProject v0.0.1 (by UserName#tag)',
            'login': login,
            'api_key': api_key
        }

        # e6_request = r.get(f'https://e621.net/posts.json?tags={args}&limit=100', headers=e621_agent)
        async with aiohttp.ClientSession(headers=e621_agent, auth=aiohttp.BasicAuth(login, api_key)) as session:
            async with session.get(f'https://e621.net/posts.json?tags={arg}&limit=100') as e6_request:
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
            embed_err = discord.Embed(title=" ⚠️ **Error!** ⚠️", description=f'Oof, Looks like there is nothing to find for `{arg}`.\nError: {e}', colour=0xff0000, timestamp=datetime.datetime.utcnow())
            embed_err.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
            return await loading.edit(embed=embed_err)

        file_ext = ["webm", "mp4", "gif", "swf"]
        if image.split('.')[-1] in file_ext:
            embed2 = discord.Embed(title="UwU | Webm, Mp4, Gif, or Swf format has been detected in post!", description=f" 🔞 e621 image found for **`{arg}`** 🔞\n\n ⬆️ **Score:** {score}\n\n:link: **Post URL:** <https://e621.net/posts/{post_id}>\n\n:link: **Video URL:** {image}", colour=discord.Color.random(), timestamp=datetime.datetime.utcnow()) # TODO cool hyperlink thing
            embed2.set_image(url=image)
            embed2.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
            return await loading.edit(content='', embed=embed2)

        embed3 = discord.Embed(title="UwU", description=f"🔞 e621 image for **`{arg}`** 🔞 \n\n_ _ \n ⬆️ **Score:** {score}\n\n:link: **[Post URL](https://e621.net/posts/{post_id})**", colour=discord.Color.random())
        embed3.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        embed3.set_image(url=image)
        await loading.edit(content='', embed=embed3)


    @e6.error
    async def on_command_error(self, ctx: SlashContext, error):
        if not isinstance(error, commands.errors.NSFWChannelRequired):
            raise error
        embed = discord.Embed(title="Error!", description="The channel this command was ran is was not a nsfw channel.\nPlease make sure to use this command in nsfw channels only.", color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"{botver} | code by Ori#6338", icon_url='https://cdn.discordapp.com/attachments/850592305420697620/850595192641683476/orio.png')
        await ctx.send(embed=embed)
    


    @cog_ext.cog_subcommand(base='tag', name='add', description='Add tags to the bots tag blacklist.', guild_ids=guild_ids)
    async def add(self, ctx: SlashContext, tag: str):
        database = sqlite3.connect('tag_blacklist.db')
        c = database.cursor()
        c.execute(f"INSERT INTO tags VALUES ('{tag}')")
        database.commit()
        database.close()
        await ctx.send('Tag successfully added to blacklist!', hidden=True)

    @cog_ext.cog_subcommand(base='tag', name='rmv', description='Remove tags from the bots tag blacklist.', guild_ids=guild_ids)
    async def rmv(self, ctx: SlashContext, tag: str):
        database = sqlite3.connect('tag_blacklist.db')
        c = database.cursor()
        c.execute(f"DELETE FROM tags WHERE tag_names LIKE '{tag}'")
        database.commit()
        database.close()
        await ctx.send('Tag successfully removed from blacklist!', hidden=True)



            
def setup(bot):
  bot.add_cog(e621Slash(bot)) 
