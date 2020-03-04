import discord


from discord.ext import commands

TOKEN = 'NjgyMTgyMTQ2ODUyNzgyMDgy.Xl-0AQ.Mtgp97lnVb9eRM79z0IQjTg-rVI'

bot = commands.Bot(command_prefix =';')

@bot.event
async def on_ready():
    print('Je suis co !')



@bot.command()
async def devoir(ctx, date, matiere, devoir):
    await ctx.send('```Les devoirs sont : Pour le {} \nEn : {}\nFaire : {}```'.format(date, matiere, devoir))

  
bot.run(TOKEN)

