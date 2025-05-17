from datetime import timedelta
from .userModeration import UserModeration
import discord

class KickModeration(UserModeration):
    
    def __init__(
        self, 
        bot,
        interaction,
        user, 
        modlog_reason,
        moderator_id
    ):
        super().__init__(bot, interaction, user, modlog_reason, 0, "Kick", moderator_id)

    async def kick_user(
        self
    ):    
        await self.interaction.guild.kick(user=self.user, reason=self.modlog_reason)
        COIN_SERVER = self.bot.get_guild(676112926918049813)
        await COIN_SERVER.kick(user=self.user, reason=self.modlog_reason)        


    async def send_log_embed(
        self,
        connection
    ):
        # Public Success Embed
        response_embed = discord.Embed(
            description=(
                f"✅ **{self.user.display_name}** has been **kicked**\n"
                f"**Reason:** {self.modlog_reason}"
            ),
            color=0x00ffff
        )

        success_message = await self.interaction.channel.send(embed=response_embed)

        # Initialize appeal message
        appeal_message = ""

        # Modlog Embed
        log_embed = discord.Embed(
            title="🚪 Kick Log",
            color=0x00ffff,
            timestamp=self.interaction.created_at
        )

        log_embed.set_author(
            name=self.interaction.guild.name,
            icon_url=str(self.interaction.guild.icon)
        )

        log_embed.add_field(
            name="👮 Moderator",
            value=f"{self.interaction.user.mention} (`{self.interaction.user.id}`)",
            inline=False
        )

        log_embed.add_field(
            name="🙍‍♂️ User Kicked",
            value=f"{self.user.mention} (`{self.user.id}`)",
            inline=False
        )

        log_embed.add_field(
            name="📄 Reason",
            value=f"```{self.modlog_reason}```",
            inline=False
        )

        log_embed.add_field(
            name="🔗 Jump to Message",
            value=f"[Click to view]({success_message.jump_url})",
            inline=False
        )

        # Send to log channel if in target guild
        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.interaction.guild.get_channel(1028869177798295632)
            appeal_message = "You may appeal this kick here: https://discord.gg/YkcvK7P2zt"

            modlogs_embed = await self.get_modlogs(
                user=self.user,
                interaction=self.interaction,
                connection=connection
            )

            self.log_embed_message = await log_channel.send(embeds=[log_embed, modlogs_embed])            
        # Attempt to DM the user
        try:
            
            await self.user.send(
                content=f"You have been **kicked** from **{self.interaction.guild.name}**.",
                embeds=[log_embed, modlogs_embed]
            )
            
            await self.user.send(
                content=f"{appeal_message}"
            )

        except:
            pass
    