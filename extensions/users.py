from discord.ext import commands
import asyncio
import discord
import files

file = files.Files()
file.setup()


class User(commands.Cog, name="User Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.member_list = None
        self.role_list = None

    @commands.command(name="displayitems", description='Displays a list of purchasable roles', help="Display all of"
                      + " purchasable roles within a guild.\n\n Format\n\n.displayitems")
    @commands.check(files.word_check)
    async def item(self, ctx):
        """This command allows for the user to be able to see what roles purchasable roles
        are available on the server."""
        if len(ctx.message.content.split()) == 1:
            role_list = await asyncio.gather(file.roles_return())
            role_list = role_list[0]
            # If the role list is bigger than zero
            if len(role_list) != 0:
                # Creates an embed
                embed_to_user = discord.Embed(title="List of Roles", description="Check out the roles you can purchase",
                                              colour=discord.Colour.purple())
                embed_to_user.set_thumbnail(
                    url="https://i.pinimg.com/originals/31/73/05/3173050e21aa147111101847d026d33d.jpg")
                # Makes a field with each purchasable role
                for key in role_list.keys():
                    if role_list[key]['enabled']:
                        embed_to_user.add_field(name=key, value="Price: " + str(role_list[key]["purchase_price"]),
                                                inline=False)
                # Sends the embed back to the user
                await ctx.send(embed=embed_to_user)
            # If there the role list is empty
            else:
                await ctx.send(f'<@{ctx.author.id}> No purchasable roles are available at this moment.')

    @commands.command(name='display', description='Displays the current points a user has', help="Display your current"
                      + " number of points that can be used for purchasing roles.\n\nFormat\n\n.display")
    @commands.check(files.word_check)
    async def display_points(self, ctx):
        """Displays the amount of points a user has currently."""
        if len(ctx.message.content.split()) == 1:
            id = str(ctx.author.id)
            # Retrieve the points from the json file and display it back to the user
            points = await asyncio.gather(file.display(id))
            points = points[0]
            await ctx.send(f'<@{ctx.author.id}> You currently have: {str(points)} points.')

    @commands.command(name='buyrole', description='This command allows a user to purchase a role', help="Buy a role"
                      + " within the guild with your points.\n\nFormat\n\n.buyrole <role>\n\nExample\n\n"
                      + ".buyrole vip")
    @commands.check(files.word_check)
    async def buy_role(self, ctx: discord.ext.commands.Context, role):
        """This command allows for a user to be able to purchase a role and will decrease the amount of current
        points they have.
        command: .buy_role <role>"""
        message = ctx.message.content.split()
        if len(message) == 2:
            member = ctx.message.author
            temp_role_list = await asyncio.gather(file.roles_return())
            temp_role_list = temp_role_list[0]
            # If the role is within the list of purchasable roles and the role is enabled to be purchased
            if role in temp_role_list.keys() and temp_role_list[role]['enabled']:
                # Gets the role from with the utility function
                role_result = discord.utils.get(ctx.guild.roles, name=role)
                # Gets the number of points from the member
                member_points = await asyncio.gather(file.display(str(member.id)))
                member_points = int(member_points[0])
                # Gets the number price of the role
                purchase_price = await asyncio.gather(file.price(role))
                purchase_price = int(purchase_price[0])
                # If the user has enough points and the role is not within the member's roles, allow for
                # a purchase to be made
                if member_points >= purchase_price and role_result not in member.roles:
                    await member.add_roles(role_result)
                    await file.buy_role(str(member.id), purchase_price)
                    current_points = member_points - purchase_price
                    await ctx.send(f'<@{ctx.author.id}> You have purchased the {role} role.\n'
                                   f'Current points: {current_points}')
                # If the member does not have enough points
                elif member_points < purchase_price and role_result not in member.roles:
                    await ctx.send(f'<@{ctx.author.id}> You do not have enough points. Current points: {member_points}'
                                   f'\nNeeded points for {role} role: {purchase_price}')
                # If the role is already in the member's roles.
                elif role_result in member.roles:
                    await ctx.send(f'<@{ctx.author.id}> You already have this role. You cannot purchase it again.')
            # If the role is not within the purchase list
            elif role not in temp_role_list.keys():
                await ctx.send(f'<@{ctx.author.id}> This role is not in the role purchase list.')
            # If the role is not purchasable
            elif not temp_role_list[role]['enabled']:
                await ctx.send(f'<@{ctx.author.id}> This role is not available for purchase')


def setup(bot):
    bot.add_cog(User(bot))
