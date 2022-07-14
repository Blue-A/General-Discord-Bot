import discord
import os
import files
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# Intents allows for a bot to subscribe to certain bucket events.
intents = discord.Intents.default()
# Allows for member caching
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
# The files that will be accessed as extensions
extensions = ['extensions.help', 'extensions.users', 'extensions.admin', 'extensions.moderation', 'extensions.general']
file = files.Files()

@bot.event
async def on_ready():
    """Called when the client is done preparing data from discord. Usually after a successful login."""
    print(f'{bot.user.name} has connected to discord!')
    for extension in extensions:
        bot.load_extension(extension)
    file.setup()
    result = await asyncio.gather(file.member_exists(bot.owner_id))
    result = result[0]
    if not result:
        await file.join(bot.owner_id)


@bot.event
async def on_member_join(member):
    """An event that occurs when the bot sees that someone has joined the guild.
    The bot will send a message out to the member who joined the guild."""
    result = await asyncio.gather(file.member_exists(member.id))
    result = result[0]
    # If the user does not exist within the member_list dictionary
    if not result:
        await file.join(member.id)


@bot.event
async def on_error(event, *args, **kwargs):
    """Writes error messages to a log."""
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled exception: {args[0]}\n')
        else:
            raise


@bot.event
async def on_command_error(ctx, error):
    """An error is sent when a user is missing a permission to send a command."""
    if isinstance(error, (commands.MissingRole, commands.MissingPermissions)):
        await ctx.send(f'<@{ctx.author.id}> {error}')


@bot.event
async def on_message(message):
    """When a user sends a message, there will be a filter to see if there are banned words or not.
    If there are banned words, they will get a warning and the message will be removed. If not, the message
    will remain within the channel."""
    if message.author == bot.user:
        return
    result = await asyncio.gather(file.check_commands(message.content.split()[0]))
    result = result[0]
    # Checking if the word is a command
    if not result:
        result = await asyncio.gather(file.check_word(message.content))
        result = result[0]
        # If the message content contains a blacklisted word
        if not result:
            # Checking if the author's id is the same as the owner id
            if message.guild.owner_id != message.author.id:
                await message.delete()
                iterator = warn_member(message.author)
                string = await iterator.__anext__()
                # If the offense count has not been reset
                if string != "0":
                    string = await iterator.__anext__()
                    await message.channel.send(string)
                # If the count has been reset, proceed to ban user
                else:
                    await iterator.__anext__()
            return
        # If the message content does not contain a blacklisted word
        else:
            await increase_points(message)
    await bot.process_commands(message)


async def warn_member(member):
    """Warns a user if they send messages with banned word(s).
    If they will be banned if they receive three offensive strikes"""
    answer = await asyncio.gather(file.offensive_warn(str(member.id)))
    answer = answer[0]
    # If the user's warning count has been reset to 0
    if answer == "0":
        yield answer
        await member.create_dm()
        await member.dm_channel.send(f'You have been banned from: {member.guild}.\nReason: Inappropriate language.')
        await member.ban()
    # If the user has a warning count above 0
    else:
        yield answer
        yield f'<@{member.id}> you are being warned for: {"Using inappropriate language"}\nYour warning count: {answer}'


async def increase_points(message):
    """Increases the points a member has when a message sent in a channel."""
    author = str(message.author.id)
    await file.increase_points(author)

bot.run(TOKEN)
