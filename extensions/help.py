import discord
from discord.ext import commands


class NewHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        """Makes a command signature that shows the prefix, name and the signature (parameters) of the command."""
        signature = getattr(command, "signature", "None")
        if signature != "None":
            string = '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
        else:
            string = '%s%s' % (self.clean_prefix, command.qualified_name)
        if len(command.description) > 1:
            string += " - " + command.description
        return string

    async def send_bot_help(self, mapping):
        """Makes an embed and sends all of the possible commands if the user has the appropriate role to see it."""
        embed = discord.Embed(title='Help Command', description="For more help on commands, please use .help <command>"
                              + " for more information.", colour=discord.Colour.blurple())
        # Loop through all of the cogs and commands to add them on the embed as a field
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            # If there are any fields, add them to the embed
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        # Get the channel and send the embed to that channel
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        """Makes an embed and shows the command if the user has the appropriate role"""
        commands = [command]
        filtered = await self.filter_commands(commands, sort=True)
        # If the command exists, add it to the embed.
        if filtered:
            embed = discord.Embed(title="Help Command", colour=discord.Colour.blurple())
            command_name = self.clean_prefix + command.qualified_name
            embed.add_field(name=command_name, value=command.help)
            channel = self.get_destination()
            await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        help_command = NewHelp()
        help_command.cog = self
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(Help(bot))
