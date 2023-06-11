import discord
from .chessTournamentModalReview import ChessTournamentModalReview

class InvalidResponse(Exception):
    pass

class ChessTournamentModal(discord.ui.Modal, title="Chess Tournament Sign-up"):
    rating = discord.ui.TextInput(
        label="What is your exact Elo/Rating?",
        style=discord.TextStyle.short,
        placeholder="Elo/Rating Here...",
        required=True,
        min_length=0,
        max_length=5
    )

    basic_rule_set = discord.ui.TextInput(
        label="Aware of the basic rules of the game? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="(Yes/No) Here...",
        required=True,
        min_length=1,
        max_length=3
    )

    time_playing_chess = discord.ui.TextInput(
        label="How long have you been playing chess?",
        style=discord.TextStyle.short,
        placeholder="Time Playing Chess Here...",
        required=True,
        min_length=3,
        max_length=10
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):

        try:
            rating_str = str(self.rating.value)
            rating_str = rating_str.replace(',', '')
            
            for num in rating_str:
                if not num.isdigit():
                    rating_str = rating_str.replace(f"{num}", '')
            
            rating_int = int(rating_str)
            
            acceptable_responses = ["yes", 'y', 'n', "no"]
            if (self.basic_rule_set.value.lower()) not in acceptable_responses:    
                raise InvalidResponse

        
        except ValueError:
            error_embed = discord.Embed(
                title="Error: Your Elo/rating was not a number. Please try again.",
                description="Note: put only a number for your elo/rating for example: 1000",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
        
        except InvalidResponse:
            error_embed = discord.Embed(
                title="Error: Invalid Input. Please try again.",
                description="Your response to the question: ``Aware of the basic rules of the game?`` was invalid. Please answer the question with a ``Yes`` or a ``No``.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                    
        sign_up_embed = discord.Embed(
            title=f"Chess Tournament Sign-up",
            color=0x00ffff
        )
        
        sign_up_embed.set_author(
            name=f"Submitted by: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        sign_up_embed.timestamp = interaction.created_at
        
        sign_up_embed.set_footer(
            text=f"The Conquerors 3 Chess Tournament Sign-up",
            icon_url=interaction.guild.icon
        )

        sign_up_embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        sign_up_embed.add_field(
            name=f"Player Elo/Rating:",
            value=f"``{rating_int}``",
            inline=False
        )

        sign_up_embed.add_field(
            name="Knows ruleset/how to move pieces?",
            value=f"``{self.basic_rule_set.value}``",
            inline=False
        )

        sign_up_embed.add_field(
            name="Playing Chess since:",
            value=f"``{self.time_playing_chess.value}``",
            inline=False
        )

        chess_sign_ups_channel = interaction.guild.get_channel(1035759149021147226)
        await chess_sign_ups_channel.send(
            content=f"{interaction.user.mention}",
            embed=sign_up_embed,
            view=ChessTournamentModalReview()
        )

        approved_embed = discord.Embed(
            title=f"Approved: Event Committee have been notified about your sign-up!",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=approved_embed,
            ephemeral=True
        )