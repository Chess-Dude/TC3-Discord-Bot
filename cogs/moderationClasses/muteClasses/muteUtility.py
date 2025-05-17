import discord, datetime

class MuteUtility:
    def __init__(
        self, 
        member, 
        duration, 
        interaction,
        time_type,
        reason
    ):
        self.member = member
        self.duration = duration
        self.interaction = interaction
        self.time_type = time_type
        self.reason = reason 
        self.log_embed_message = None

    async def is_staff(
        self
    ):
        """
        Checks if user is staff. Returns true if they are.
        """
        staff_role_id_list = [1072233470606200853,
                              351074813055336458,
                              351166789700550679,
                              363125947635073025,
                              743302990001340559,
                              554152645192056842,
                              743115435821498460,
                              419333829891850250,
                              363500459203231746
                              ]
        
        for role_id in staff_role_id_list:
            staff_role = self.interaction.guild.get_role(role_id)
            
            if staff_role in self.member.roles:
                response_embed = discord.Embed(
                    description=f"✅ {self.member.display_name} is a staff member! | Failed to mute.", 
                    colour=0x00ffff
                )
                self.success_message = await self.interaction.channel.send(embed=response_embed)
                return True
        
        return False

    async def mute_user(
        self
    ):
        """
        Does all the muting process. Invoked by perm mute and mute command.
        """
        try:
            muted_role = self.interaction.guild.get_role(351091626950787084)
        
        except:
            muted_role = discord.utils.get(self.interaction.guild.roles, name="muted")
        await self.member.add_roles(muted_role)
        duration_seconds = 0
        if self.time_type != None:
            if self.time_type.lower() == "minutes":
                time_duration = datetime.timedelta(minutes=self.duration)
                duration_seconds = self.duration * 60


            elif self.time_type.lower() == "hours":
                time_duration = datetime.timedelta(hours=self.duration)
                duration_seconds = self.duration * 3600

            else:
                time_duration = datetime.timedelta(minutes=self.duration)
                duration_seconds = self.duration * 60

            await self.member.timeout(time_duration)

        await self.send_mute_log_embed()
        return duration_seconds
        
    async def send_mute_log_embed(
        self
    ):
        """
        sends mute log embed to log channel and user.
        """
        response_embed = discord.Embed(
            description=f"✅ {self.member.display_name} has been muted for {self.duration} {self.time_type} | {self.reason}", 
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
            name="Member Muted",
            value=f"{self.member.mention}, ``{self.member.id}``",
            inline=False
        )           

        log_embed.add_field(
            name="Reason Of Mute",
            value=f"``{self.reason}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Duration Of Mute",
            value=f"``{self.duration} {self.time_type}``",
            inline=False
        )           
        
        log_embed.add_field(
            name="Jump", 
            value = f"[Go to message!]({success_message.jump_url})",
            inline=False
        )

        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.interaction.guild.get_channel(1028869177798295632)
            appeal_message = "You may appeal this mute here: https://discord.gg/YkcvK7P2zt"
            self.log_embed_message = await log_channel.send(embed=log_embed)
            
        try:
            await self.member.send(
                content=f"You have been muted at the ``{self.interaction.guild.name}`` server. {appeal_message}",
                embed=log_embed
            )
        except:
            pass
    
    async def unmute_user(
        self
    ):
        """
        unmutes user and sends unmute log embed
        """
        muted_role = self.interaction.guild.get_role(351091626950787084)        
        await self.member.remove_roles(muted_role)
        await self.member.timeout(None)
        await self.send_unmute_log_embed()

    async def send_unmute_log_embed(
        self
    ):
        """
        send unmute log embed
        """
        unmute_log_embed = discord.Embed(
            color=0x00ffff, 
            timestamp=self.interaction.created_at
        )

        unmute_log_embed.set_author(
            name=f"{self.interaction.guild.name}",
            icon_url=f"{self.interaction.guild.icon}"
        )

        unmute_log_embed.add_field(
            name="Member Unmuted",
            value=f"{self.member.mention}, ``{self.member.id}``",
            inline=False
        )           
                
        await self.member.send(
            content="You have been unmuted.",
            embed=unmute_log_embed
        )

        if self.log_embed_message != None:
            unmute_log_embed.add_field(
                name="Jump", 
                value = f"[Go to message!]({self.log_embed_message.jump_url})",
                inline=False
            )       

        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.interaction.guild.get_channel(351084557929283585)
            await log_channel.send(embed=unmute_log_embed)