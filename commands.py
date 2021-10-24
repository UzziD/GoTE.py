import os
from discord.ext import commands
from discord.ext.commands.core import is_owner

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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
    
    @logspirit.error
    async def logspirit_error(self,ctx,error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments provided. Format: !log <item name> <count of item>")
        else:
            print("error on command: {}".format(ctx.command))
            await ctx.send("There was an error!")


    @commands.command(name='shutdown')
    @is_owner()
    async def shutdown(self, ctx):
        print("shutting down")
        await self.bot.close()

    @shutdown.error
    async def shutdown_error(self,ctx,error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of the bot can shut it down.")
        else:
            print("error shutting down: {}".format(error))
            await ctx.send("Error shutting down, check terminal.")