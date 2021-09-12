import os
import random
from discord.ext import commands
from pyparsing import Suppress, Group, Word, CaselessLiteral, Literal, alphas, nums
from dotenv import load_dotenv

dice_exp = Group(Word(nums).setResultsName("number").setParseAction(lambda toks:int(toks[0])) 
        + Suppress(CaselessLiteral("d"))
        + Word(nums).setResultsName("faces").setParseAction(lambda toks:int(toks[0])))
arth_exp = Literal("+") | Literal("-")
roll_exp = dice_exp + ( arth_exp + dice_exp)[...]

bot = commands.Bot(command_prefix="!")

@bot.command(name='roll')
async def rool(ctx, *args):
    diceCommand = "".join(args)
    print (diceCommand)
    query = roll_exp.parseString(diceCommand)
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
            roll = mod * random.randrange(1, current.faces) * current.number
            total += roll
            message = f"{'+' if mod > 0 else '-'}{current.number}d{current.faces}({roll}){message}"
    message = f"roll = {total} : {message}"    
    print(message)
    await ctx.send(message)
load_dotenv()
bot.run(os.environ.get("DISCORD_DARK_MATTER_BOT_TOKEN"))