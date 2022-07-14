from discord.ext import commands
import asyncio
import discord
import files
import re

file = files.Files()

class Moderation(commands.Cog, name="Moderation Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban', description='Bans a single member', help="Bans a single member within the guild.\n\n"
                      + "Format\n\n.ban @user\n.ban <user id>\n\nExamples\n\n.ban @Bob\n.ban 130403208253278145")
    @commands.has_permissions(ban_members=True)
    @commands.check(files.word_check)
    async def ban_member(self, ctx: discord.ext.commands.Context, user_id):
        """Bans a selected member from the guild
        A reason may be added for banning the member."""
        admin_message = ctx.message.content.split()
        if len(admin_message) >= 2:
            match = re.match(r'<@([0-9]+)>$', user_id)
            match_two = re.match(r'[0-9]+', user_id)
            if match or match_two:
                member = discord.utils.get(ctx.guild.members, id=int(re.sub(r'\D', '', str(user_id))))
                if member and ctx.author.id != member.id:
                    # The member exists within the guild and the author is not the admin
                    ban_pass = await asyncio.gather(self.check(ctx, member))
                    ban_pass = ban_pass[0]
                    # If owner is the author of the message
                    if ctx.author.id == ctx.guild.owner_id:
                        ban_pass = True
                    # If an attempt to ban the bot is made
                    if self.bot.user.id == member.id or member.id == ctx.guild.owner_id:
                        ban_pass = False
                    # If the member is able to be banned
                    if ban_pass:
                        # If there is a reason attached to the ban
                        if len(admin_message) > 2:
                            await member.create_dm()
                            await member.dm_channel.send(
                                f"You have been banned from {ctx.guild.name}.\nReason: {admin_message[2:]}")
                            await member.ban(reason=admin_message[2:])
                        # If there is not a reason attached to the ban
                        else:
                            await member.create_dm()
                            await member.dm_channel.send(f"You have been banned from {ctx.guild.name}.\nReason: None")
                            await member.ban()
                        await ctx.send(admin_message[1] + " is successfully banned.")
                    # If the member is the owner or the bot
                    else:
                        await ctx.send(f'<@{str(ctx.author.id)}> You do not have permission to ban {admin_message[1]}')
                # If the admin is trying to ban his/her self
                elif member and ctx.author.id == member.id:
                    await ctx.send(f'<@{str(ctx.author.id)}> You should not try to ban yourself!')
                # If the member does not exist within the guild
                elif not member:
                    await ctx.send(f'<@{ctx.author.id}> This member does not exist within the guild')
            # If the user ID does not pass the regular expressions
            else:
                await ctx.send(f'<@{ctx.author.id}> Please enter the correct format for a user.')

    @commands.command(name='multiban', description='Bans mulitple members', help="Bans multiple members.\n\nFormats"
                      + "\n\n.multiban <user id>\n<user id>.....\n.multiban @user @user @user"
                      + "\n\nExamples\n\n.mutliban 130403208253278145\n"
                      + "130403208253274155\n430403208453270146\n\n.multiban @Bob @Sarah @Tim")
    @commands.has_permissions(ban_members=True)
    @commands.check(files.word_check)
    async def ban_members(self, ctx: discord.ext.commands.Context, user_ids):
        """Bans multiple members from the guild."""
        # Gets rid of duplicate user id's
        admin_message = list(dict.fromkeys(ctx.message.content.split()))
        guild = ctx.guild
        author = ctx.author
        string = None
        ban_entries = await ctx.guild.bans()
        # Loops through all of the messages from the given user ID's
        for i in range(1, len(admin_message)):
            # Checks if the user id contains a letter
            match = re.match(r'<@([0-9]+)>$', admin_message[i])
            match_two = re.match(r'[0-9]+', admin_message[i])
            # If the user id contains a letter or the length is not 18, inform that the user id not valid
            if not match and not match_two:
                # If the string is not made yet.
                if not string:
                    string = "Here is a list of possible bans: \n" + admin_message[i] + \
                             " is not a valid user id."
                # If the string already exists, append to it.
                else:
                    string += "\n" + admin_message[i] + " is not a valid user id."
            else:
                # Removes special characters
                id = int(re.sub(r'\D', '', str(admin_message[i])))
                found = False
                # Looping through all of the banned ID's to see if there is a match.
                for banned_member in ban_entries:
                    if banned_member.user.id == id:
                        found = True
                        break
                # If a banned user is found, do not ban them again.
                if found:
                    # If the string is not made yet.
                    if not string:
                        string = "Here is a list of possible bans: \n" + str(id) + " is already banned."
                    # If the string is already made.
                    else:
                        string += "\n" + str(id) + " is already banned."

                else:
                    # Find the member with the utility function
                    member = discord.utils.get(guild.members, id=id)
                    # The member exists within the guild and the author is not the admin
                    if member and str(author.id) != str(id) and id != ctx.guild.owner_id:
                        # Checks if the client user is able to ban the target user
                        ban_pass = await asyncio.gather(self.check(ctx, member))
                        ban_pass = ban_pass[0]
                        # Allows for server owner to ban no matter what.
                        if ctx.author.id == ctx.guild.owner_id:
                            ban_pass = True

                        # If an attempt to ban the bot is made.
                        if self.bot.user.id == id or member.id == ctx.guild.owner_id:
                            ban_pass = False

                        # If the string is not made yet.
                        if not string:
                            # If the user is able to get banned
                            if ban_pass:
                                string = "Here is a list of possible bans: \n" + str(member.id) + \
                                        " received a ban."
                                await member.ban()
                            else:
                                string = "Here is a list of possible bans: \nYou do not have permission to ban " \
                                        + str(member.id)
                        # If the string is made already
                        else:
                            if ban_pass:
                                string += "\n" + str(member.id) + " received a ban."
                                await member.ban()
                            else:
                                string += "\nYou do not have permission to ban " + str(member.id)
                    # If the admin/owner is trying to ban his/her self
                    elif str(author.id) == str(id):
                        # If the string is not made yet.
                        if not string:
                            string = "Here is a list of possible bans: \nYou should not attempt to ban yourself!"
                        # If the string is already made
                        else:
                            string += "\nYou should not attempt to ban yourself!"
                    # If the member does not exist within the guild
                    elif not member:
                        # If the string is not made yet.
                        if not string:
                            string = "Here is a list of possible bans: \n" + str(member.id) + \
                                     " does not exist within the guild."
                        # If the string is already made.
                        else:
                            string += str(member.id) + " does not exist within the guild."
                    # If an attempt to the ban server owner is made
                    elif id == ctx.guild.owner_id:
                        if not string:
                            string = "Here is a list of possible bans: \nYou cannot ban the server owner!"
                        # If the string is made already
                        else:
                            string += "\nYou cannot ban the server owner!"
        await ctx.send(string)

    @commands.command(name='unban', description='Unbans one member', help="Unbans one member from the guild\n\n"
                      + "Format\n\n.unban <user id>\n\nExample\n\n.unban 130403208253278145")
    @commands.has_permissions(ban_members=True)
    @commands.check(files.word_check)
    async def unban_member(self, ctx: discord.ext.commands.Context, user_id):
        """Unbans a selected member from the guild.
        A reason may be added."""
        admin_message = ctx.message.content.split()
        # If the user entered a message longer than 1
        if len(admin_message) >= 2:
            # If the user did not enter a valid ID
            if not user_id.isnumeric() or len(user_id) != 18:
                await ctx.send("You entered a invalid possible user ID.")
            # If the user entered a valid ID
            else:
                id = int(user_id)
                ban_entries = await ctx.guild.bans()
                found = False
                # Loop through all of the bans
                for ban_entry in ban_entries:
                    # A user is found within the banned entries
                    if ban_entry.user.id == id:
                        found = True
                        await ctx.send(str(ban_entry.user.id) + " is successfully unbanned.")
                        # Only ban with no reason
                        if len(admin_message) == 2:
                            await ctx.guild.unban(ban_entry.user)
                        # Ban with a reason submitted
                        elif len(admin_message) > 2:
                            await ctx.guild.unban(ban_entry.user, reason=admin_message[2:])
                        break
                if not found:
                    await ctx.send("The user of this ID is not banned.")

    @commands.command(name='multiunban', description='Unbans multiple members', help="Unbans mutliple members\n\n"
                      + "Format\n\n.multiunban <user id>\n<user id>.....\n\nExample\n\n.multiunban 130403208253278145\n"
                      + "130403208253274155\n430403208453270146")
    @commands.has_permissions(ban_members=True)
    @commands.check(files.word_check)
    async def unban_members(self, ctx: discord.ext.commands.Context, user_ids):
        """Unbans selected members from the guild"""
        admin_message = ctx.message.content.split()
        # Retrieving all of the banned members.
        ban_entries = await ctx.guild.bans()
        string = None
        # Loop through all of the spaced strings
        for i in range(1, len(admin_message)):
            found = False
            # If the message is not numeric or not a length of 18, it is not a valid user id
            if not admin_message[i].isnumeric() or len(admin_message[i]) != 18:
                # If the string has not been made yet
                if not string:
                    string = "Here is a list of possible unbans: \n" + admin_message[i] + " is not a valid" + \
                             " user id"
                # If the string has been made already
                else:
                    string += "\n" + admin_message[i] + " is not a valid user id"
            else:
                id = int(admin_message[1])
                # Loop through all of the banned entries
                for ban_entry in ban_entries:
                    # If there is a matching id, break out of the loop
                    if ban_entry.user.id == id:
                        found = True

                if not found:
                    # If the string is not made already.
                    if not string:
                        string = "Here is a list of possible unbans: \n" + str(id) + " is not banned."
                    # If the string is made already.
                    else:
                        string += "\n" + str(id) + " is not banned."
                else:
                    # If the string is not made already.
                    if not string:
                        string = "Here is a list of possible unbans: \n" + str(id) + " is successfully unbanned."
                    # If the string is made already.
                    else:
                        string += "\n" + str(id) + " is successfully unbanned."
        await ctx.send(string)

    @commands.command(name='mute', description='Mutes a member for a certain amount of minutes', help="Mutes a member"
                      + " for a specified amount of time.\n\nFormats\n\n.mute @user <minutes>\n.mute <user id>"
                      + " <minutes>\n\nExamples\n\n.mute @Bob 3\n.mute 430403208453270146 3")
    @commands.check(files.word_check)
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx: discord.ext.commands.Context, user, minutes):
        """This command allows you to mute a member for any particular reason"""
        # If the message is three arguments, minutes is numeric and at least one minute
        if len(ctx.message.content.split()) == 3 and minutes.isnumeric() and int(minutes) >= 1:
            match = re.match(r'<@([0-9]+)>$', user)
            match_two = re.match(r'[0-9]+', user)
            # If the user entered an invalid user id because of alpha/special characters
            if not match and not match_two:
                await ctx.send("Please enter a valid user ID.")
            else:
                id = int(re.sub('\D', '', user))
                check = True
                # Checking if an attempt to mute the guild owner is made
                if ctx.author.id == ctx.guild.owner_id:
                    check = True
                # Checking if an attempt to mute the bot is made
                if id == self.bot.user.id or id == ctx.guild.owner_id:
                    check = False
                # If the user can be muted.
                if check:
                    # If the author is muting themselves
                    if ctx.author.id != id:
                        member = discord.utils.get(ctx.guild.members, id=id)
                        # If member exists
                        if member:
                            check = await asyncio.gather(self.check(ctx, member))
                            check = check[0]
                            role = discord.utils.get(ctx.guild.roles, name='mute')
                            # If the selected member has lower roles than the message author
                            if check:
                                if role and role not in member.roles:
                                    # Adds the muted role to the user
                                    await member.add_roles(role)
                                    if minutes == '1':
                                        await ctx.send(f'<@{member.id}> is muted for {minutes} minute.')
                                    else:
                                        await ctx.send(f'<@{member.id}> is muted for {minutes} minutes.')
                                    count = 0
                                    total = int(minutes) * 60
                                    # Loop until the designated time.
                                    while True:
                                        count += 1
                                        if count == total:
                                            break
                                        if role not in member.roles:
                                            break
                                        await asyncio.sleep(1)
                                    # If the role exists within the user's list of roles after looping
                                    if role in member.roles:
                                        await member.remove_roles(role)
                                        await ctx.send(f'<@{member.id}> is now unmuted.')
                                # If the role does not exist within the guild
                                elif not role:
                                    await ctx.send(
                                        "The 'mute' role does not exist. Please add one with the correct permissions.")
                                # If the user is already muted.
                                else:
                                    await ctx.send(f'<@{member.id}> is already muted.')
                            # If the selected member cannot be muted due to roles high or the same as message author.
                            else:
                                await ctx.send(f'<@{ctx.author.id}> You cannot mute this member because they have'
                                               f' roles high or the same as yours.')
                        # If the member does not exist within the guild
                        else:
                            await ctx.send("This member does not exist within the guild")
                    # If a client user makes attempt to mute themselves
                    else:
                        await ctx.send(f'<@{ctx.author.id}> You cannot mute yourself!')
                # If a client user attempts to mute the bot or the server owner
                else:
                    await ctx.send(f'<@{ctx.author.id}> The user <@{id}> cannot be muted')
        # If the client user does not enter a number
        elif not minutes.isnumeric():
            await ctx.send("The minutes you entered is not numeric. Please enter a proper number.")
        # If an attempt to mute a user for less than one minute is made
        elif minutes.isnumeric() and int(minutes) < 1:
            await ctx.send("You can only mute a member for one or more minutes.")

    @commands.command(name='unmute', description='Unmutes a member', help="Unmutes a member within the guild\n\n"
                      + "Formats\n\n.unmute @User\n.unmute <user id>\n\nExamples\n\n.unmute @Bob\n.unmute"
                      + " 430403208453270146")
    @commands.check(files.word_check)
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx: discord.ext.commands.Context, user):
        """Unmutes a member if they are already muted."""
        if len(ctx.message.content.split()) == 2:
            match = re.match(r'<@([0-9]+)>$', user)
            match_two = re.match(r'[0-9]+', user)
            # If the user entered an invalid user id because of alpha/special characters
            if not match and not match_two:
                await ctx.send("Please enter a valid user ID.")
            else:
                user_id = int(re.sub('\D', '', user))
                member = discord.utils.get(ctx.guild.members, id=user_id)
                role = discord.utils.get(ctx.guild.roles, name='mute')
                # Removing a muted role from a user
                if member and role and role in member.roles:
                    # Checking the context author's roles against the selected user
                    check = await asyncio.gather(self.check(ctx, member))
                    check = check[0]
                    # If the owner is issuing the command
                    if ctx.author.id == ctx.guild.owner_id:
                        check = True
                    # If the selected user is the bot
                    if self.bot.user.id == id or member.id == ctx.guild.owner_id:
                        check = False
                    # If the user is able to be unmuted
                    if check:
                        await member.remove_roles(role)
                        await ctx.send(f'<@{member.id}> has been unmuted')
                    # If the user cannot be unmuted
                    else:
                        await ctx.send(f'<@{ctx.author.id}>You do not have permission to unmute <@{id}>')
                # If the user does not exist within the guild
                elif member:
                    await ctx.send("The member does not exist. So you cannot unmute your chosen user.")
                # If the mute role does not exist
                elif not role:
                    await ctx.send("The mute role does not exist within the guild.")
                # If the user does not have the mute role within their list of roles
                elif member and role not in member.roles:
                    await ctx.send("This member is not muted at the moment.")

    @commands.command(name="warn", description='Warn a member and will mute after 3 warnings', help="Warns a member for"
                      + " misconduct. A mute command will be activated once the user has been given 3 warnings.\n\n"
                      + "Formats\n\n.warn @user <reason>\n.warn <user id> <reason>\n\nExamples\n\n"
                      + ".warn @Bob Spamming the general channel.\n.warn 430403208453270146 Spamming the"
                      + " general channel.")
    @commands.check(files.word_check)
    @commands.has_guild_permissions(mute_members=True)
    async def warn(self, ctx: discord.ext.commands.Context, user, reason):
        """Warns a user by sending a message out to them. If they have three warnings, they will
        be muted for 60 minutes."""
        message = ctx.message.content.split()
        if len(message) == 3:
            match = re.match(r'<@([0-9]+)>$', user)
            match_two = re.match(r'[0-9]+', user)
            # If the user entered an invalid user id because of alpha/special characters
            if not match and not match_two:
                await ctx.send("Please enter a valid user ID.")
            else:
                user_id = int(re.sub('\D', '', user))
                check = True
                # Checking if an attempt to mute the guild owner is made
                if user_id == ctx.guild.owner_id:
                    check = False
                # Checking if an attempt to mute the bot is made
                if user_id == self.bot.user.id:
                    check = False
                member = discord.utils.get(ctx.guild.members, id=user_id)
                # If the user is able to be warned
                if check:
                    # If the member exists within the guild, perform a warn operation
                    if member:
                        # Checks if the client user is able to ban the target user
                        check = await asyncio.gather(self.check(ctx, member))
                        check = check[0]
                        if check:
                            answer = await asyncio.gather(file.warn(member.id))
                            answer = answer[0]
                            # If the user's warning count has been reset to 0
                            if answer == "0":
                                await ctx.send(
                                    f'<@{member.id}> has been warned three times now. You are muted for 60 minutes.')
                                await self.mute(ctx, user, "60")
                            # If the user has a warning count above 0
                            else:
                                await ctx.send(
                                    f'<@{member.id}> you are being warned for: {reason}\nYour warning count: {answer}')
                        else:
                            await ctx.send(f'<@{ctx.author.id}> You do not have permission to warn <@{id}>')
                    # If the user does not exist
                    else:
                        await ctx.send("This member does not exist")
                # If the user cannot be warned
                else:
                    await ctx.send(f'<@{ctx.author.id}> You cannot warn <@{id}>')

    @commands.command(name="addblacklist", description='Adds a word to the blacklist', help="Adds a blacklisted word"
                      + " that users will not be able to say.\n\nFormat\n\n.addblacklist <word>\n\nExample\n\n"
                      + ".addblacklist test")
    @commands.has_permissions(manage_channels=True)
    async def add_blacklist_word(self, ctx: discord.ext.commands.Context, word):
        """Adds a blacklisted word to a JSON file"""
        message = ctx.message.content.split()
        if len(message) == 2:
            result = await asyncio.gather(file.add_word(word))
            result = result[0]
            # If the word does not exist within the black list
            if result:
                await ctx.send("The word is added to the black list")
            # If the word already exists within the black list
            else:
                await ctx.send("The word already exists within the black list")

    @commands.command(name="checkblacklist", description="Displays all of the blacklisted words",
                      help="Checks all of the blacklisted words.\n\nFormat\n\n.checkblacklist")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def check_words(self, ctx: discord.ext.commands.Context):
        """Returns a list of blacklisted words"""
        word_list = await asyncio.gather(file.get_word_list())
        word_list = word_list[0]
        # If there is a word list
        if word_list:
            await ctx.send("Current banned words:\n" + "\n".join(word_list))
        # If there is not a word list
        else:
            await ctx.send(f'<@{ctx.author.id}> No banned words recorded. Please add some words to the black list.')

    @commands.command(name="removeword", description="Removes blacklisted word from list", help="Removes a blacklisted"
                      + " word.\n\nFormat\n\n.removeword <word>\n\nExample\n\n.removeword peanuts")
    @commands.has_permissions(manage_channels=True)
    async def remove_word(self, ctx: discord.ext.commands.Context, word):
        """Removes a blacklisted word"""
        if len(ctx.message.content.split()) == 2:
            result = await asyncio.gather(file.remove_word(word))
            result = result[0]
            # If the word was removed.
            if result:
                await ctx.send(f'<@{ctx.author.id}> The word was removed from the blacklist')
            # If the word was not removed.
            else:
                await ctx.send(f'<@{ctx.author.id}> The word does not exist within the blacklist')

    async def check(self, ctx, member):
        """Checks the roles between two users to see if they have the same permission levels"""
        check = True
        for role in ctx.author.roles:
            if role.name != "@everyone":
                for member_role in member.roles:
                    if member_role.name != "@everyone" and role <= member_role:
                        check = False
                        break
        return check


def setup(bot):
    bot.add_cog(Moderation(bot))