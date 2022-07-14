from discord.ext import commands
import discord
import re
import files
import asyncio

file = files.Files()


class Admin(commands.Cog, name="Admin Commands"):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.advertisement = False
        self.inner_ad = False
        self.message = "Custom Message"
        self.muted = []

    @commands.command(name='deletechannel', description='Deletes an existing channel within the guild', help="Deletes"
                      " an entire channel from the guild if it exists. If not, a message indicating that the" +
                      " channel does not exist will be sent. A category and channel will be required for channel"
                      " deletion.\n\nFormat\n\n.deletechannel <channel>\n\n" +
                      "Example\n\n.deletechannel #introductions")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx: discord.ext.commands.Context, channel):
        """Bot command that deletes an entire channel.
        command: .delete_channel <name of channel>"""
        if len(ctx.message.content.split()) == 2:
            match = re.match(r'<#([0-9]+)>', channel)
            # If the channel matches the appropriate REGEX
            if match:
                channel = re.sub('\D', '', channel)
                channel = discord.utils.get(ctx.guild.channels, id=int(channel))
                # If the channel exists
                if channel:
                    await channel.delete()
                    await ctx.send(f'<@{ctx.author.id}> Channel: {channel} has been deleted.')
                # If the channel does not exist
                else:
                    await ctx.send(f'<@{ctx.author.id}> This channel does not exist within the guild')
            # If the channel does not match the regular expression
            else:
                await ctx.send(f'<@{str(ctx.author.id)}> Please enter a valid channel.')

    @commands.command(name='createchannel', description='Creates a channel within the guild', help="Creates a channel" +
                      " within a category if it does not already exist.The channel type will need to be specified"
                      "when using this command.\n\nFormat\n\n.create_channel <category_id> <channel> <channel "
                      "type>\n\n " + "Channel types\n\n'v' or 'V' for voice channel\n't' or 'T' for text-channel"
                      + "\n\nExample\n\n.create_channel 867104176653374493 introductions T")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx: discord.ext.commands.Context, category, channel, channel_type):
        """Bot command that creates an entire channel.
        command: .create_channel <name of category> <name of channel> <type of channel>"""
        message = ctx.message.content.split()
        # If the user sent a message containing four strings
        if len(message) == 4:
            category_match = re.match(r'[0-9]+', category)
            # If the category matches the REGEX
            if category_match:
                category_id = re.sub(r'\D', '', category)
                category_result = discord.utils.get(ctx.guild.categories, id=int(category_id))
                # If the category exists
                if category_result:
                    channel_result = discord.utils.get(category_result.channels, name=channel)
                    # If the channel does not exist within the category
                    if not channel_result:
                        # Making a text channel
                        if channel_type == "t" or channel_type == "T":
                            await category_result.create_text_channel(channel)
                            await ctx.send(
                                f'The text channel {channel} is create within the {category_result.name} category')
                        # Making a voice channel
                        elif channel_type == "v" or channel_type == "V":
                            await category_result.create_voice_channel(channel)
                            await ctx.send(
                                f'The voice channel {channel} is create within the {category_result.name} category')
                        # Invalid channel selection
                        else:
                            await ctx.send(f'{channel_type} is not a valid selection for channel type'
                                           f' enter either: \n"v" to make a voice-channel\n"t"'
                                           f' to make a text-channel')
                    # If the channel exists within the category
                    else:
                        await ctx.send(f'<@{ctx.author.id}> The channel already within the category.')
                # If the category does not exist within the guild
                else:
                    await ctx.send(f'The category {category} does not exist within the guild')
            # If there is non-numeric characters within the category
            else:
                await ctx.send(f'<@{ctx.author.id}> Please enter a valid category id without non-numeric characters.')

    @commands.command(name='addrole', description='Assign a role to a user', help="Enter a " +
                      "user and a role in order to assign them a role within the guild if it exists.\n"
                      "\nFormat\n\n.addrole <user> <role>\n.addrole <user_id> <role>\n\n"
                      "Examples\n\n.addrole @Bob admin\n.addrole 130403208253278145 admin")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def user_adding_role(self, ctx: discord.ext.commands.Context, user, role):
        """Allows a staff member to add a role.
        command: .add_role <user id> <role>"""
        if len(ctx.message.content.split()) == 3:
            match = re.match(r'<@([0-9]+)>$', user)
            match_two = re.match(r'[0-9]+', user)
            # If an invalid user ID was given
            if match or match_two:
                role_result = discord.utils.get(ctx.guild.roles, name=role)
                # If the role exists within the guild
                if role_result:
                    member = discord.utils.get(ctx.guild.members, id=int(re.sub(r'\D', '', user)))
                    # If the member exists within the guild
                    if member:
                        add_pass = await asyncio.gather(self.check_role(ctx, role_result, "MTE"))
                        add_pass = add_pass[0]
                        # If the user initiating the command is the owner
                        if ctx.author.id == ctx.guild.owner_id:
                            add_pass = True
                        # If the selected user is a bot
                        if member.id == self.bot.user.id:
                            add_pass = False
                        # If the user is able to add another user with the a role with similar permission level
                        if add_pass:
                            # If the role does not exist within the member's roles
                            if role_result not in member.roles:
                                await member.add_roles(role_result)
                                await ctx.send(f'This role has been added to <@{member.id}>.')
                            # If the role exists within the member's roles
                            else:
                                await ctx.send(f'<@{member.id}> already has this role.')
                        # If the user cannot add another to this role
                        else:
                            await ctx.send(f'<@{ctx.author.id}> You are not allowed to add another user with'
                                           f'this role with your current permission level.')
                    # If no member was found with the corresponding user ID
                    else:
                        await ctx.send(f'<@{ctx.author.id}> This member does not exist within the guild')
                # If the role was not found within the guild
                else:
                    await ctx.send(f'<@{ctx.author.id}> The role entered does not exist.')
            else:
                await ctx.send(f'<@{ctx.author.id}> Please enter a valid user.')

    @commands.command(name="removerole", description="Removes role from a user", help="Removes a role"
                      + " from an existing user if the user and role exist.\n\nFormat\n\n.removerole <user> <role>\n" +
                      ".removerole <user_id> <role>\n\nExamples\n\n.removerole @Bob admin\n.removerole" +
                      " 130403208253278145 admin")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx: discord.ext.commands.Context, user, role):
        """Removes a member's role
        Command: .remove_role <user id> <role>"""
        if len(ctx.message.content.split()) == 3:
            match = re.match(r'<@([0-9]+)>$', user)
            match_two = re.match(r'[0-9]+', user)
            # If the user matches either REGEX
            if match or match_two:
                member = discord.utils.get(ctx.guild.members, id=int((re.sub(r'\D', '', user))))
                role_result = discord.utils.get(ctx.guild.roles, name=role)
                # If the role does not exist within the guild
                if not role_result:
                    await ctx.send(f'<@{ctx.author.id}> The role entered does not exist within the guild.')
                # If the member exists
                elif member:
                    remove_pass = await asyncio.gather(self.check_role(ctx, role_result, "MORE"))
                    remove_pass = remove_pass[0]
                    # If the user initiating the command is the owner
                    if ctx.author.id == ctx.guild.owner_id:
                        remove_pass = True
                    # If the selected member is a bot
                    if member.id == self.bot.user.id:
                        remove_pass = False
                    # If the user is able to remove the role from another member
                    if remove_pass:
                        # If the role exists within the member's role and the member isn't a owner.
                        if role_result in member.roles:
                            await member.remove_roles(role_result)
                            await ctx.send(f'{role} role has been removed from <@{str(member.id)}>')
                        # If the member does not have the role.
                        else:
                            await ctx.send(f'<@{ctx.author.id}> This member does not have this role')
                    # If the user is not able to remove the role from another member
                    else:
                        await ctx.send(f'<@{ctx.author.id}> You are not allowed to remove this '
                                       f'role from <@{member.id}>')
                # If the member does not exist within the guild
                else:
                    await ctx.send(f'<@{ctx.author.id}> The member does not exist within the guild.')
            else:
                await ctx.send(f'<@{ctx.author.id}> Please enter a valid user.')

    @commands.command(name="deleterole", description='Deletes a role within the guild', help="Deletes a role within" +
                      " the guild if it exists.\n\nFormat\n\n.deleterole <role>\n\nExample\n\n.deleterole admin")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def delete_role(self, ctx: discord.ext.commands.Context, role):
        """Removes the role of
        command: .remove_role <name of role>"""
        role_result = discord.utils.get(ctx.guild.roles, name=role)
        if len(ctx.message.content.split()) == 2:
            if role_result:
                remove_pass = await asyncio.gather(self.check_role(ctx, role_result, "Equal"))
                remove_pass = remove_pass[0]
                # If the user initiating the command is the owner
                if ctx.author.id == ctx.guild.owner_id:
                    remove_pass = True
                # If the user is able to remove this role
                if remove_pass:
                    await asyncio.gather(file.remove_role(role))
                    await role_result.delete()
                    await ctx.send(f'<@{ctx.author.id}> The role {role} has been deleted.')
                # If the user is not able to remove this role
                else:
                    await ctx.send(f'<@{ctx.author.id}> You do not have permission to remove this role.')
            else:
                await ctx.send(f'<@{ctx.author.id}> This role does not exist within the guild.')

    @commands.command(name='createrole', description='Creates a role within the guild', help="Creates a role within"
                      " the guild. A role and a colour selection will need to be specified.\n\nColour selection\n\n"
                      + "red\nblue\npurple\ngold\nteal\nrandom\n\nFormat\n\n.createrole <role> <colour selection>\n\n"
                      + "Example\n\n.createrole TestRole Blue")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def create_role(self, ctx: discord.ext.commands.Context, role, colour):
        """A command that creates a role within the guild
        command: .create_role <name of role> <colour selection>"""
        role_result = discord.utils.get(ctx.guild.roles, name=role)
        if len(ctx.message.content.split()) == 3:
            # If the role already exists
            if role_result:
                await ctx.send(f'<@{ctx.author.id}> This role already exists.')
            else:
                # If and elif states picking which selection for a role colour.
                colour = colour.lower()
                if colour == 'purple':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.purple())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                elif colour == 'red':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.red())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                elif colour == 'blue':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.blue())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                elif colour == 'gold':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.gold())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                elif colour == 'random':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.random())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                elif colour == 'teal':
                    await ctx.guild.create_role(name=role, colour=discord.Colour.teal())
                    await ctx.send(f'<@{ctx.author.id}> The role: {role} was created.')
                else:
                    await ctx.send(f'<@{ctx.author.id}> entered a invalid colour selection. Please pick '
                                   f'one:\npurple\nred\nblue\ngold\nrandom\nteal')

    @commands.command(name='createcategory',description='Creates a category within the guild',help="Creates a" +
                      "category if it does not exist within the guild.\n\nFormat\n\n.createcategory <category>\n\n" +
                      "Example\n\n.createcategory welcome")
    @commands.has_permissions(manage_channels=True)
    async def create_category(self, ctx: discord.ext.commands.Context, category):
        category_name = ctx.message.content.split()
        if len(ctx.message.content.split()) >= 2:
            category_name = " ".join(category_name[1:])
            category_name = category_name.lower()
            category_result = discord.utils.get(ctx.guild.categories, name=category_name)
            # If the category does not exist, create it within the guild.
            if not category_result:
                await ctx.guild.create_category(category_name)
                await ctx.send(f'<@{ctx.author.id}> The category {category_name} has been created.')
            # If the category exists, alert the author of the message.
            else:
                await ctx.send(f'<@{ctx.author.id}> The category {category_name} already exists within the guild.')

    @commands.command(name='deletecategory', description='Creates a category within the guild', help="Deletes a"
                      + " category within the guild if it exists.\n\nFormat\n\n.deletecategory <category>\n\n"
                      + "Example\n\n.deletecategory welcome")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def delete_category(self, ctx: discord.ext.commands.Context, category):
        """Deletes a category within a channel."""
        category_match = re.match(r'[0-9]+', category)
        if len(ctx.message.content.split()) == 2:
            if category_match:
                category_result = discord.utils.get(ctx.guild.categories, id=int(category))
                # If the category does not exist
                if not category_result:
                    await ctx.send(f'<@{ctx.author.id}> The category does not exist within the guild.')
                else:
                    # Deletes channels within a category
                    for channel in category_result.channels:
                        await channel.delete()
                    await category_result.delete()
                    await ctx.send(f'<@{ctx.author.id}> The "{category_result.name}" category has been deleted.')

    @commands.command(name='setpoints', description='Sets the number of points to buy a role', help="Sets the number"
                      + " of points for a role so that it be purchased within the guild.\n\nFormat\n\n.setpoints"
                      + " <role> <points>\n\nExample\n\n.setpoints test_role 50000")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def set_points(self, ctx: discord.ext.commands.Context, role, points):
        """This command adds a role to the roles.json file and sets the number of points."""
        # If the user entered three strings
        message = ctx.message.content.split()
        if len(message) == 3:
            # Obtain the role through the utility function if it exists
            role_result = discord.utils.get(ctx.guild.roles, name=role)
            # Retrieve the role list
            role_list = await asyncio.gather(file.roles_return())
            role_list = role_list[0]
            # If the role has not been set for purchase yet.
            if role_result and points.isnumeric() and role not in role_list:
                await file.set_points("yes", role, int(points))
                await ctx.send(f'<@{ctx.author.id}> ' + "This role's price has been set and is available for purchase "
                                                        "by members.")
            # If the role already has been set for purchase
            elif role_result and points.isnumeric() and role in role_list:
                await file.set_points("no", role, int(points))
                await ctx.send(f'<@{ctx.author.id}> The new purchase price is set for this role.')
            # If the user did not enter a proper number
            elif not points.isnumeric():
                await ctx.send(f'<@{ctx.author.id}> You did not enter a valid number of points')
            # If the role does not exist within the guild
            elif not role_result:
                await ctx.send(f'<@{ctx.author.id}> The role does not exist')

    @commands.command(name='changepoints', description='Changes the number of points a member currently has', help=""
                      + "Changes the number of points a user has.\n\nFormats\n\n.changepoints @User <points>"
                      + "\n.changepoints <user id> <points>\n\nExamples\n\n.changepoints @Bob 1000"
                      + "\n.changepoints 130403208253278145 1000")
    @commands.check(files.word_check)
    @commands.has_permissions(administrator=True)
    async def modify_points(self, ctx: discord.ext.commands.Context, user, points):
        """Changes the number of points a member currently has."""
        if len(ctx.message.content.split()) == 3 and points.isnumeric():
            match = re.search('[a-zA-Z]', user)
            id = re.sub(r'\D', '', str(user))
            # If the user entered an invalid user id because of alpha/special characters
            if match or len(id) != 18:
                await ctx.send("Please enter a valid user ID.")
            else:
                member = discord.utils.get(ctx.guild.members, id=int(id))
                # If the member exists within the guild, set their number of points
                if member:
                    await file.change_points(str(member.id), int(points))
                    await ctx.send(f"{member.display_name}'s number of points has changed.")
                # The user does not exist within the guild
                else:
                    await ctx.send(f'<@{ctx.author.id}> This member does not exist within the guild.')
        # If the points argument is not numeric
        elif not points.isnumeric():
            await ctx.send(f"<@{ctx.author.id}> You did not enter a number. "
                           f"Make sure you enter only numbers for the number of points.")

    @commands.command(name="startad", description='Activates advertisement within a channel', help="Activates an"
                      " advertisement message that will be displayed throughout a channel. In order to"
                      " change the advertisement message, use the .changead command.\n\nFormat\n\n"
                      " .startad <channel>\n\nExample\n\n.startad #general")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def activate_advertisement(self, ctx: discord.ext.commands.Context, channel):
        """Activates an advertisement within a channel"""
        if len(ctx.message.content.split()) == 2:
            match = re.match(r'<#([0-9]+)>', channel)
            # If a REGEX match was found
            if match:
                channel_result = discord.utils.get(ctx.guild.channels, id=int(re.sub('\D','', channel)))
                # If the channel exists and advertisement may not be going on at the current moment.
                if channel_result and not self.advertisement:
                    self.advertisement = True
                    count = 0
                    await ctx.send(f'<@{ctx.author.id}> Advertisement has begun within ' + channel_result.name)
                    await channel_result.send(self.message)
                    # Loop through every 30 minutes to display an ad
                    while True:
                        count += 1
                        # Loop until 1800 and display an advertisement
                        if count == 1800 and self.advertisement:
                            count = 0
                            await channel_result.send(self.message)
                        await asyncio.sleep(1)
                        # If the advertisement is finished
                        if not self.advertisement:
                            break
                # If advertisement is currently in operation
                elif self.advertisement:
                    await ctx.send(f'<@{ctx.author.id}> Advertisement is currently activated. Please deactivate it '
                                   f'before using this command.')
                # If the channel does not exist within the guild
                else:
                    await ctx.send(f'<@{ctx.author.id}> Channel does not exist for advertisement.')
            # If a REGEX match was not found
            else:
                await ctx.send(f'<@{ctx.author.id}> Please use the correct format when selecting a channel')

    @commands.command(name="endad", description='Ends the advertisement within a channel', help="Stops the"
                      " the advertisement within a channel if it is currently active.\n\nFormat\n\n.endad")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def end_advertisement(self, ctx: discord.ext.commands.Context):
        """Ends advertisement within a channel"""
        if self.advertisement:
            self.advertisement = False
            await ctx.send(f'<@{ctx.author.id}> Advertisement has deactivated.')
        else:
            await ctx.send(f'<@{ctx.author.id}> Advertisement is not currently active.')

    @commands.command(name="changead", description='Changes the advertisement message', help="Changes the"
                      " the advertisement message that can be shown within a channel. Use the .startad command"
                      " to do so.\n\nFormat\n\n.changead <message>\n\nExample\n\n.changead Hello 123\nTesting"
                      " this is a test in order to show this command.\nEnter like this to write a message.")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def change_ad_message(self, ctx: discord.ext.commands.Context, ad_message):
        """Changing the advertisement message within the channel"""
        message = ctx.message.content.split(" ", 1)
        self.message = message[1]
        await ctx.send("The advertisement message has changed")

    @commands.command(name="checkad", description='Displays the advertisement message', help="Displays the"
                      " the advertisement message.\n\nFormat\n\n.checkad")
    @commands.check(files.word_check)
    @commands.has_permissions(manage_channels=True)
    async def check_message(self, ctx: discord.ext.commands.Context):
        """Returns the stored message advertisement message."""
        if len(ctx.message.content.split()) == 1:
            await ctx.send(self.message)

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

    @commands.command(name="usertojson", description="Adds user to members.json", help="Adds a user to the members.json"
                      + " if they do not already exist\n\nFormats\n\n.usertojson <member>\n.usertojson <member id>"
                      + "\n\nExamples\n\n.usertojson @Bob\n.usertojson 130403208253278145")
    @commands.has_permissions(administrator=True)
    @commands.check(files.word_check)
    async def usertojson(self, ctx: discord.ext.commands.Context, member: str):
        """Adds a user to members.json if the user does not exist."""
        if len(ctx.message.content.split()) == 2:
            match = re.match(r'<@([0-9]+)>$', member)
            match_two = re.match(r'[0-9]+', member)
            # If the member matches the pattern
            if match or match_two:
                user_id = int(re.sub('\D', '', member))
                result = await asyncio.gather(file.member_exists(user_id))
                result = result[0]
                # If the member already exists within the JSON file
                if result:
                    await ctx.send(f'<@{ctx.author.id}> This member already exists within the json file')
                # If the member does not exist within the JSON file
                else:
                    await file.join(user_id)
                    await ctx.send(f'<@{ctx.author.id}> The member is added to the json file')
            # If the member does not match the pattern
            else:
                await ctx.send(f'<@{ctx.author.id}> Please enter the correct format for this command')

    async def check_role(self, ctx, role, operator):
        """Compares an author's roles with a role.
        Uses a specific operator to use a specific for loop"""
        check = False
        # If the operator is more than equal
        if operator == "MTE":
            for member_role in ctx.author.roles:
                if member_role.name != "@everyone":
                    if member_role >= role:
                        check = True
                        break
        # If the operator is more than
        else:
            for member_role in ctx.author.roles:
                if member_role.name != "@everyone":
                    if member_role > role:
                        check = True
                        break
        return check


def setup(bot):
    bot.add_cog(Admin(bot))
