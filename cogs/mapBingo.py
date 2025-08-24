import discord
from discord import app_commands as app
from discord.ext import commands
import json
from typing import Literal, Any
maps = Literal[
    "Sandstone Cog", "Last Red City", "Double Mansion", "Mars", "Endceladus", 
    "World", "Mesa", "Eygptian Expedition", "Long Islands", "Two Islands Map", 
    "Mansion", "Magma Pools", "Sandy Floors", "Skymap", "Maze", "Germany Map",
    "Mainland", "Archipelago", "Passage", "Continent", "Igneous Islands/Magma",
    "Spain", "Arctic Canal Map", "Gem Mine", "Middle East", "Mainland"
]
started = False
file = "./bingo_answers.json"
async def save_answer(answer: Any):
    answers = {"answer": answer}
    with open(file, "w") as f:
        json.dump(answers, f)
async def save_choice(userid: int, choice: Any):
    with open(file, "r") as f:
        choices = json.load(f)
    if str(userid) not in choices:
        choices[str(userid)] = {}
    choices[str(userid)] = choice
    with open(file, "w") as f:
        json.dump(choices, f)
async def get_choice(userid: int):
    try:
        with open(file, "r") as f:
            choices = json.load(f)
        if str(userid) not in choices:
            return None
        return choices[str(userid)]
    except FileNotFoundError:
        return None    
async def get_answer():
    return await get_choice("answer") #type: ignore

class BingoCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test")
        
    a = app.Group(name = "guess", description = "Guessing game")
    @a.command(name = "start", description = "Starts the game")
    async def start(self, ctx: discord.Interaction, correct: maps):
        #assert (not isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel, discord.ForumChannel, discord.CategoryChannel))) or ctx.channel != None
        await ctx.channel.send(f"{correct}") #type: ignore
        await save_answer(correct)
        await ctx.response.send_message(
            content="Task Completed",
            ephemeral=True
        )
    @a.command(name = "guess", description = "Guesses the answer")
    async def guess(self, ctx: discord.Interaction, guess: maps):
        global started
        if started:
            await ctx.response.send_message("The game has not started yet!", ephemeral = True)
            return
        await save_choice(ctx.user.id, guess)
        await ctx.response.send_message("Success", ephemeral = True)
    @a.command(name = "end", description = "Ends the game")
    async def end(self, ctx: discord.Interaction):
        global started
        if not started:
            await ctx.response.send_message("The game has not started yet!", ephemeral = True)
            return
        await ctx.response.send_message("Success", ephemeral = True)
        await ctx.channel.send("The game has ended!")
        started = False
    @a.command(name="get", description="Gets your answer")
    async def get(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"Your answer is {await get_choice(ctx.user.id)}", ephemeral = True)
    @a.command(name="getall", description="Gets all answers")
    async def getall(self, ctx: discord.Interaction):
        newline = '\n'
        await ctx.response.send_message(f"All answers are: \n{[(user, answer, newline) for user, answer in json.load(open(file, 'r'))]}", ephemeral = True)
    @a.command(name="answer", description="Gets the answer")
    async def answer(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"The answer is {await get_answer()}", ephemeral = True)
    @a.command(name="getuser", description="Gets a user's answer")
    async def getuser(self, ctx: discord.Interaction, user: discord.User):
        await ctx.response.send_message(f"{user.mention}'s answer is {await get_choice(user.id)}", ephemeral = True)
    @a.command(name="winners", description="Gets the winners")
    async def winners(self, ctx: discord.Interaction, private:bool = True):
        correct = await get_answer()
        winners = []
        answers = dict(json.load(open(file, "r")))
        print(answers)
        for user, answer in zip(answers.keys(), answers.values()):
            if answer == correct and user != "answer":
                winners.append(user)
                print(f"{user} is a winner with {answer}!")  
        newline = '\n'
        if winners == []:
            await ctx.response.send_message("There are no winners!", ephemeral = True)
            return
        winlist = ""
        for winner in winners:
            winlist += f"<@{winner}>\n"
        await ctx.response.send_message(f"The winner{'s are' if len(winners) != 1 else ' is'}: \n{winlist}", ephemeral = private)