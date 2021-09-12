from pyparsing import Suppress, Group, Word, CaselessLiteral, Literal, alphas, nums
import pprint
import random
pp = pprint.PrettyPrinter()
dice_exp = Group(Word(nums).setResultsName("number").setParseAction(lambda toks:int(toks[0])) 
        + Suppress(CaselessLiteral("d"))
        + Word(nums).setResultsName("faces").setParseAction(lambda toks:int(toks[0])))
arth_exp = Literal("+") | Literal("-")
roll_exp = dice_exp + ( arth_exp + dice_exp)[...]

query = roll_exp.parseString("3D20+2D12-1d4")

total = 0
mod = 1
message = "";
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
        print(message)
message = f"roll = {total} : {message}"
print(message)