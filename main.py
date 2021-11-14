import discord
from discord.ext import commands
import asyncio
from clashroyaleapi import clashRoyale
import os
import json
from dotenv import load_dotenv
import twitterapi

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
            description='Overview of our clan',
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
                description='use .clanmember command to search individuals', # clanmember not created yet
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


@bot.command(aliases=['add_reminder'])
async def create_reminder(ctx, *, reminder: str):
    username = ctx.message.author.name
    with open("reminders.txt", "r") as file:
        current_reminders = json.load(file)
    if username not in current_reminders:
        current_reminders[username] = []
    current_reminders[username].append(reminder)
    with open("reminders.txt", "w") as file:
        json.dump(current_reminders, file)
    await ctx.send(f"Reminder made \n```{reminder}```")


def reminder_reader():
    with open("reminders.txt", "r") as reminder_file:
        result = json.load(reminder_file)

    return result


@bot.command()
async def reminders(ctx):
    result = reminder_reader()
    embed = discord.Embed(
        title='Reminders',
        description='Reminders made by members for the server',
        colour=discord.Colour.green()

    )
    for i in result:
        embed.add_field(name= f'Reminder by {i}', value= "\n".join(result[i]), inline= False)
    await ctx.send(embed=embed)


@bot.command()
async def clear_reminder(ctx, *, message):
    found = False
    with open("reminders.txt", "r") as f:
        data = json.load(f)
    for element in data:
        if message in data[element]:
            data[element].remove(message)
            await ctx.send(f"Reminder cleared by <@{ctx.message.author.id}>```{message}```")
            found = True
    for element in list(data.keys()):
        if len(data[element]) == 0:
            del data[element]
    with open("reminders.txt", "w") as f:
        json.dump(data, f)
    if not found:
        await ctx.send("Reminder not found")


@bot.command()
async def ratio(ctx):
    tweet = twitterapi.find_ratio()
    await ctx.send('https://twitter.com/twitter/statuses/' + str(tweet))


load_dotenv()
discord_token = os.getenv('discord_token')
bot.run(discord_token)
