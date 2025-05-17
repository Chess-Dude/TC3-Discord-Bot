from datetime import timedelta
from .userModeration import UserModeration
import discord

class MuteModeration(UserModeration):
    
    def __init__(
        self, 
        bot,
        interaction,
        user, 
        modlog_reason,
        raw_mute_length,
        damage_taken,
        moderator_id
    ):
        super().__init__(bot, interaction, user, modlog_reason, damage_taken, "Mute", moderator_id)
        self.raw_mute_length = raw_mute_length
        self.mute_length = None

    def calculate_mute_time(
        self
    ):
        unit_map = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days'}
        unit = self.raw_mute_length[-1]

        try:
            value = int(self.raw_mute_length[:-1])
        except ValueError:
            return False

        self.mute_length = timedelta(**{unit_map[unit]: value})
        return self.mute_length

    async def mute_user(
        self
    ):
        try:
            muted_role = self.interaction.guild.get_role(351091626950787084)
        
        except:
            muted_role = discord.utils.get(self.interaction.guild.roles, name="muted")
        
        await self.user.timeout(self.mute_length)

    def update_muted_db(
        self
    ):
        pass

    async def send_log_embed(
        self,
        connection
    ):
        # Public Success Embed
        response_embed = discord.Embed(
            description=(
                f"✅ **{self.user.display_name}** has been **muted** for **{self.raw_mute_length}**\n"
                f"**Reason:** {self.modlog_reason}"
            ),
            color=0x00ffff
        )

        success_message = await self.interaction.channel.send(embed=response_embed)

        # Initialize appeal message
        appeal_message = ""

        # Modlog Embed
        log_embed = discord.Embed(
            title="🔇 Mute Log",
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
            name="🙍‍♂️ User Muted",
            value=f"{self.user.mention} (`{self.user.id}`)",
            inline=False
        )

        log_embed.add_field(
            name="📄 Reason",
            value=f"```{self.modlog_reason}```",
            inline=False
        )

        log_embed.add_field(
            name="⏳ Duration",
            value=f"```{self.raw_mute_length}```",
            inline=False
        )

        log_embed.add_field(
            name="💢 Damage Taken",
            value=f"```{self.damage_taken}```",
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
            appeal_message = "You may appeal this mute here: https://discord.gg/YkcvK7P2zt"

            modlogs_embed = await self.get_modlogs(
                user=self.user,
                interaction=self.interaction,
                connection=connection
            )

            self.log_embed_message = await log_channel.send(embeds=[log_embed, modlogs_embed])

        # Attempt to DM the user
        try:
            await self.user.send(
                content=f"You have been **muted** in **{self.interaction.guild.name}**. Note if you accumulate **10 active damage points**, you __will be banned__",
                embeds=[log_embed, modlogs_embed]
            )

            await self.user.send(
                content=f"{appeal_message}",
            )
        except:
            pass

    
    async def perm_mute_user(
        self,
    ):
        try:
            muted_role = self.interaction.guild.get_role(351091626950787084)
        
        except:
            muted_role = discord.utils.get(self.interaction.guild.roles, name="muted")
        
        await self.user.add_roles(muted_role)
