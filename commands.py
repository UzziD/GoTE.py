import os
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(name='hello')
    async def testfunc(self, ctx):
        await ctx.send("hi!")

    @commands.command(name='log')
    async def logspirit(self, ctx, item: str, count: int):
        try:
            db = open("log.csv", 'a')
            try:
                db.write("{},{}\n".format(item, count))
                await ctx.send("Logged: {} {}".format(count, item))
            except Exception as e:
                await ctx.send("Error writing to file.")
                print("Exception occured: {}".format(e))
            finally:
                db.close()
        except Exception as e:
            await ctx.send("Error opening file.")
            print("Exception occured: {}".format(e))



        #await ctx.send("you've logged {} {}".format(count, item))
        #print()