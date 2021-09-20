import os
import random
from discord.ext import commands
from pyparsing import Suppress, Group, Word, CaselessLiteral, Literal, alphas, nums
from dotenv import load_dotenv

dice = Group(Word(nums).setResultsName("number").setParseAction(lambda toks:int(toks[0])) 
        + Suppress(CaselessLiteral("d"))
        + Word(nums).setResultsName("faces").setParseAction(lambda toks:int(toks[0])))
arth = Literal("+") | Literal("-")
roll_grammar = dice + ( arth + dice)[...]

bot = commands.Bot(command_prefix="!")

@bot.command(name='roll')
async def roll_command(ctx, *args):
    roll_arguments = "".join(args)
    query = roll_grammar.parseString(roll_arguments)
    total = 0
    mod = 1
    message = ""
    query = query[::-1]
    while len(query) > 0 :
        current = query.pop()
        if current == "+":
            mod = 1
        elif current == "-":
            mod = -1
        else:   
            rolls = [] 
            for _ in range(0,current.number): 
                roll = 1
                if (current.faces > 1):
                    roll = random.randrange(1, current.faces)
                rolls.append(roll)
            rolls_str = "+".join(f"{roll}" for roll in rolls)
            total_rolls = sum(rolls)
            total += total_rolls * mod
            message = f"{message} {'+' if mod > 0 else '-'}{current.number}d{current.faces}({total_rolls}={rolls_str})"
    message = f"{total} = {message}"    
    print(f"Send roll {roll_arguments} command response {message}")
    await ctx.send(message)
load_dotenv()
bot.run(os.environ.get("DISCORD_DARK_MATTER_BOT_TOKEN"))