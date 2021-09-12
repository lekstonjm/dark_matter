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
    while len(query) > 0 :
        current = query.pop()
        if current == "+":
            mod = 1
        elif current == "-":
            mod = -1
        else:      
            current_roll = mod * random.randrange(1, current.faces) * current.number
            total += current_roll
            message = f"{'+' if mod > 0 else '-'}{current.number}d{current.faces}({current_roll}){message}"
    message = f"roll = {total} : {message}"    
    print(message)
    await ctx.send(message)
load_dotenv()
bot.run(os.environ.get("DISCORD_DARK_MATTER_BOT_TOKEN"))