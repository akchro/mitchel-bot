import discord
from discord.ext import commands
import asyncio
import random
import os
import json
from dotenv import load_dotenv
import twitterapi
from clashroyaleapi import clashRoyale
from gifeditor import create_gif

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(brief='spam mitchell')  # this command is just to mess with a friend :)
async def mitchell_spam(ctx):
    for i in range(10):
        await ctx.send("<@622273993843408916>")
        await asyncio.sleep(1)


@bot.command(brief='get clan info',
             description='use .ourclan members to get member info')  # specific to my clan "Bruh Clan Cool"
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
                description='use .clanmember command to search individuals',  # clanmember not created yet
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


@bot.command(aliases=['add_reminder'], brief="create reminder")
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


@bot.command(brief='shows all reminders made')
async def reminders(ctx):
    result = reminder_reader()
    embed = discord.Embed(
        title='Reminders',
        description='Reminders made by members for the server',
        colour=discord.Colour.green()

    )
    for i in result:
        embed.add_field(name=f'Reminder by {i}', value="\n".join(result[i]), inline=False)
    await ctx.send(embed=embed)


@bot.command(brief='clears a created reminder',
             description='clears a reminder that you put\n\nex:\n.clearreminder wash dishes         clears the "wash dishes" reminder')
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


@bot.command(brief="ratio")
async def ratio(ctx):
    tweet = twitterapi.find_ratio()
    await ctx.send('https://twitter.com/twitter/statuses/' + str(tweet))


@bot.command(brief='use .help addword for more help adding words',
             description='adds words to the wordsalad phrase: "name when thing verb"\nname adds a name\nthing adds a thing\nverb adds a verb\n\nex:.addword name poggers')
async def addword(ctx, word_type, *, word):
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
    if word not in words[word_type]:
        if word_type == "name":
            words["name"].append(word)
            if word not in words["thing"]:
                words["thing"].append(word)
        else:
            words[word_type].append(word)
        await ctx.send(f"new {word_type} created")
    else:
        await ctx.send(f"{word_type} was already there")
    with open('wordlist.json', 'w') as f:
        json.dump(words, f)


@bot.command(brief='create a great phrase')
async def wordsalad(ctx):
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
        name = random.choice(words['name'])
        thing = random.choice(words['thing'])
        verb = random.choice(words['verb'])
    await ctx.send(f"{name} when {thing} {verb}")


@bot.command(brief='see all salad words and gifs')
async def salads(ctx):
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
        names = words['name']
        things = words['thing']
        verbs = words['verb']
        gifs = words['gif']
    await ctx.send(f"```py\nNames:\n{names}\n\nThings:\n{things}\n\nVerbs:\n{verbs}\n\nGifs:\n{gifs}```")


@bot.command()
async def delsalad(ctx, word, *, message):
    found = False
    with open('wordlist.json', 'r') as f:
        data = json.load(f)
    for element in data:
        if message in data[element]:
            data[element].remove(message)
            await ctx.send(f"{element} cleared by <@{ctx.message.author.id}>```{message}```")
            found = True
    with open("wordlist.json", "w") as f:
        json.dump(data, f)
    if not found:
        await ctx.send("Word not found")


@bot.command()
async def addgif(ctx, link):
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
    if link not in words["gif"]:
        if "https://" in link:
            words["gif"].append(link)
            await ctx.send("gif added")
        else:
            await ctx.send("Not a link!")
    else:
        await ctx.send("Link already there")
    with open('wordlist.json', 'w') as f:
        json.dump(words, f)


@bot.command()
@commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
async def gifsalad(ctx):
    processing = await ctx.send("Processing")
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
    name = random.choice(words['name'])
    thing = random.choice(words['thing'])
    verb = random.choice(words['verb'])
    gif = random.choice(words["gif"])
    message = f"{name} when {thing} {verb}"
    big = create_gif(gif, message)
    if big != "Big":
        await ctx.send(file=discord.File('temp.gif'))
        await processing.delete()
    else:
        await ctx.send(f"The gif used is way too big: ```{gif}``` deleting gif from list")
        with open('wordlist.json', 'r') as f:
            data = json.load(f)
        for element in data:
            if gif in data[element]:
                data[element].remove(gif)
        with open("wordlist.json", "w") as f:
            json.dump(data, f)



@bot.command()
async def github(ctx):
    await ctx.send("Go check out the repository for this bot! https://github.com/24Chromosones/mitchel-bot")


load_dotenv()
discord_token = os.getenv('discord_token')
bot.run(discord_token)
