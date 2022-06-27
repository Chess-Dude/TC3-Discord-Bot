from discord import Interaction, app_commands
from discord.ext import commands
from discord.app_commands import AppCommandError

class errorHandlerAppCommands(commands.Cog):
    def __init__(
        self, 
        bot: commands.Bot
        ):
            self.bot = bot

            # setting the handler
            bot.tree.on_error = self.on_app_command_error

  # the error handler
    async def on_app_command_error(
        self,
        interaction: Interaction,
        error: AppCommandError
        ):
            if isinstance(
                error, 
                app_commands.errors.MissingRole
                ):
                    await interaction.response.send_message(
                        content=f"Error: You are missing the required role to run this command.", 
                        ephemeral=True)

            elif isinstance(
                error, 
                app_commands.errors.MissingPermissions
                ):
                    await interaction.response.send_message(
                        content=f"Error: You are missing the needed permissions to run this command.", 
                        ephemeral=True)

            elif isinstance(
                error, 
                app_commands.errors.CommandOnCooldown
                ):
                    await interaction.response.send_message(
                        content=f"Error: Command on cooldown, try again in {int(int(error.retry_after)/60)}m{int(error.retry_after)%60}s.", 
                        ephemeral=True)
            
            elif isinstance(
                error, 
                app_commands.errors.CheckFailure
                ):
                    await interaction.response.send_message(
                        content=f"Error: You are missing the needed permissions to run this command. Please retry this command in the appropriate channel.", 
                        ephemeral=True)

            elif isinstance(
                error, 
                ZeroDivisionError
                ):
                    pass

            else:
                await interaction.response.send_message("Error: Unknown error occured. <@621516858205405197>")
                print(str(error))
    
async def setup(bot):
    await bot.add_cog(errorHandlerAppCommands(bot))