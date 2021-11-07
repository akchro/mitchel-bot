import discord
from discord.ext import commands
import asyncio
from clashroyaleapi import clashRoyale
import os

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command()  # this command is just to mess with a friend :)
async def mitchell_spam(ctx):
    for i in range(10):
        await ctx.send("<@622273993843408916>")
        await asyncio.sleep(1)


@bot.command() # specific to my clan "Bruh Clan Cool"
async def ourclan(ctx, *args):
    if len(args) == 0:
        cr = clashRoyale()
        clan_dict = cr.get_clan()
        embed = discord.Embed(
            title='Bruh Clan Cool',
            description='description',
            colour=discord.Colour.blue()

        )
        embed.set_footer(text="poggers")
        for i in clan_dict:
            if i != "memberList":
                embed.add_field(name=i, value=clan_dict[i], inline=True)
        await ctx.send(embed=embed)
    if len(args) == 1:
        cr = clashRoyale()
        clan_dict = cr.get_clan()
        if args[0] == "members":
            await ctx.send("This takes a little bit", delete_after=3)
            embed = discord.Embed(
                title='Top 20 members based on trophies',
                description='use .clanmember command to search individuals',
                colour=discord.Colour.blue()

            )
            embed.set_footer(text="poggers")
            try:
                for i in range(20):
                    embed.add_field(name=cr.clan_members()[i]["name"],
                                    value=f"trophies: {cr.clan_members()[i]['trophies']}", inline=True)
            except IndexError:
                pass  # makes it so it works on under 20 members
            await ctx.send(embed=embed)


bot.run(os.environ["discord-token"])
