from discord.ext import commands
import discord
import aiohttp
import io
import files
import json
import re

file = files.Files()


class General(commands.Cog, name="General Commands"):
    def __init__(self, bot):
        self.bot = bot
        # Opening up the json file with the points for each member
        with open('./JSON/members.json', 'r') as f:
            try:
                self.member_list = json.load(f)
            # If the file does not exist within the bot
            except FileNotFoundError:
                print("member_list file does not exist")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='greet', description="Sends a user a greeting gif", help="Sends a user a greeting GIF.\n\n"
                      + "Formats\n\n.greet @user\n.greet <user id>\n\nExamples\n\n.greet @Bob\n.greet"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def greet_user(self, ctx: discord.ext.commands.Context, user: str):
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches that fit REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Utility function that gets a member from the guild
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the member exists within the guild, send a GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://i.imgur.com/yQ18as3.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is greeting <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is greeting " + user
                            await ctx.send(content=message, file=discord.File(data, "yQ18as3.gif"))
                # If the member does not exist within the guild, send the following message
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='cry', description="Sends a user a crying gif", help="Sends a user a crying GIF.\n\n"
                      + "Formats\n\n.cry @user\n.cry <user id>\n\nExamples\n\n.cry @Bob\n.cry"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def cry(self, ctx: discord.ext.commands.Context, user: str):
        """Sends another user a crying GIF"""
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches that fit a REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Uses utility function to get a member from the guild
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the member exists within the guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://c.tenor.com/q9V98YHPZX4AAAAC/anime-umaru.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is crying <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is crying " + user
                            await ctx.send(content=message, file=discord.File(data, "anime-umaru.gif"))
                # If the member does not exist within the guild, send the following message.
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='laugh', description="Sends a user a laughing gif", help="Sends a user a laughing GIF.\n\n"
                      + "Formats\n\n.laugh @user\n.laugh <user id>\n\nExamples\n\n.laugh @Bob\n.laugh"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def laugh(self, ctx: discord.ext.commands.Context, user: str):
        """Sends a laughing GIF to another user"""
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches that fit REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Utility function to get member from guild
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If a member exists within a guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                                "https://i.kym-cdn.com/photos/images/original/000/619/204/8c0.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is laughing <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is laughing " + user
                            await ctx.send(content=message, file=discord.File(data, "8c0.gif"))
                # If a member does not exist within a guild, send the following message...
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='blowkiss', description='Sends a user a blowing kiss gif', help="Sends a user a greeting"
                      + " GIF\n\nFormats\n\n.blowkiss @user\n.blowkiss <user id>\n\nExamples"
                      + "\n\n.blowkiss @Bob\n.blowkiss 130403208253278145")
    @commands.check(files.word_check)
    async def blow_kiss(self, ctx: discord.ext.commands.Context, user: str):
        """Sends a blowing kiss GIF to another user """
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If a user entered matches to REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Utility function to get a member
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If a member exists within a guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                                "https://i.gifer.com/origin/3c/3c50e6c814eae8623065e4ddc76a32eb.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is blowing a kiss to <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is blowing a kiss to " + user
                            await ctx.send(content=message,
                                           file=discord.File(data, "3c50e6c814eae8623065e4ddc76a32eb.gif"))
                # If a member does not exist within a guild, send the following message...
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='dance', description="Sends a user a dancing gif", help="Sends a user a dancing GIF.\n\n"
                      + "Formats\n\n.dancing @user\n.dance <user id>\n\nExamples\n\n.dance @Bob\n.dance"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def dance(self, ctx: discord.ext.commands.Context, user: str):
        """Sends a dancing GIF to another user"""
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches the REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Find the user by the utility function
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the user exists within the guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://c.tenor.com/50FYjgJB64IAAAAC/chika-fujiwara.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is dancing <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is dancing " + user
                            await ctx.send(content=message, file=discord.File(data, "chika-fujiwara.gif"))
                # If the user does not exist within the guild, tell the user the member does not exist
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='angry', description="Sends a user an angry gif", help="Sends a user an angry GIF.\n\n"
                      + "Formats\n\n.angry @user\n.greet <user id>\n\nExamples\n\n.angry @Bob\n.angry"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def angry(self, ctx: discord.ext.commands.Context, user):
        """Sends an angry gif to another user """
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches the REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Find the user by the utility function
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the user exists within the guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("http://31.media.tumblr.com/71deee902dbf433e900c1da751942345"
                                               "/tumblr_mmnfkbq0OI1s2mvo5o1_500.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is angry <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is angry " + user
                            await ctx.send(content=message,
                                           file=discord.File(data, "tumblr_mmnfkbq0OI1s2mvo5o1_500.gif"))
                # If the user does not exist within the guild, tell the user the member does not exist
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='blush', description="Sends a user a blushing gif", help="Sends a user a blushing GIF.\n\n"
                      + "Formats\n\n.blush @user\n.blush <user id>\n\nExamples\n\n.blush @Bob\n.blush"
                      + " 130403208253278145")
    @commands.check(files.word_check)
    async def blush(self, ctx: discord.ext.commands.Context, user: str):
        """Sends a blushing gif to another user"""
        match = re.match(r'<@([0-9]+)>$', user)
        match_two = re.match(r'[0-9]+', user)
        # If the user entered matches the REGEX criteria
        if match or match_two:
            id = re.sub(r'\D', '', user)
            if ctx.author.id != int(id):
                # Find the user by the utility function
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the user exists within the guild, send the GIF
                if member:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://i.imgur.com/GrbQs8N.gif") as resp:
                            data = io.BytesIO(await resp.read())
                            if user[0] != "<":
                                message = "<@" + str(ctx.author.id) + "> is blushing <@" + user + ">"
                            else:
                                message = "<@" + str(ctx.author.id) + "> is blushing " + user
                            await ctx.send(content=message, file=discord.File(data, "GrbQs8N.gif"))
                # If the user does not exist within the guild, tell the user the member does not exist
                else:
                    await ctx.send(f'<@{str(ctx.author.id)}> The user you tried to use this command with '
                                   f'does not exist.')


def setup(bot):
    bot.add_cog(General(bot))
    arr = []
    # Makes a list of commands from the bot
    for command in bot.commands:
        arr.append("." + str(command))
    with open('./JSON/commands.json', 'w') as w:
        try:
            json.dump(arr, w)
        except FileNotFoundError:
            print("commands.json file not found. Add this file within the JSON directory.")
