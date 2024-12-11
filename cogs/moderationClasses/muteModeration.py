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
        self
    ):
        response_embed = discord.Embed(
            description=f"✅ {self.user.display_name} has been muted for {self.raw_mute_length} | {self.modlog_reason}", 
            colour=0x00ffff
        )
        
        success_message = await self.interaction.channel.send(embed=response_embed)
        appeal_message = ''

        log_embed = discord.Embed(
            color=0x00ffff, 
            timestamp=self.interaction.created_at
        )
        
        log_embed.set_author(
            name=f"{self.interaction.guild.name}",
            icon_url=f"{self.interaction.guild.icon}"
        )

        log_embed.add_field(
            name="Moderator",
            value=f"{self.interaction.user.mention}, ``{self.interaction.user.id}``",
            inline=False
        )

        log_embed.add_field(
            name="User Muted",
            value=f"{self.user.mention}, ``{self.user.id}``",
            inline=False
        )           

        log_embed.add_field(
            name="Reason Of Mute",
            value=f"``{self.modlog_reason}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Duration Of Mute",
            value=f"``{self.raw_mute_length}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )

        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.interaction.guild.get_channel(1028869177798295632)
            appeal_message = "You may appeal this mute here: https://goo.gl/forms/40zjxwBgD9RaV4Lh1"
            self.log_embed_message = await log_channel.send(embed=log_embed)
            
        try:
            await self.member.send(
                content=f"You have been muted at the ``{self.interaction.guild.name}`` server. {appeal_message}",
                embed=log_embed
            )
        except:
            pass
    