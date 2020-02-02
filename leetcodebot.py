import discord
from discord.ext import commands
import asyncio
import Classmate

#TOKEN = open("leetcodebottoken.txt", "rt")
TOKEN = "TOKEN_HERE"


bot = commands.Bot(command_prefix='.')

classmates = []



@bot.event
async def on_ready():
    print("LeetCodeBot is ready.")
    print("Logged in as {0.user}".format(bot))

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def add_topics(ctx, *, in_text):
    topics = in_text.split(", ")
    user = ctx.message.author.display_name
    id = ctx.message.author.id
    for person in classmates:
        if person.name == user:
            for topic in topics:
                person.topics.append(topic)
            return
    else:
        newClassMate = Classmate.ClassMate(user, id)
        for topic in topics:
            newClassMate.topics.append(topic)
        classmates.append(newClassMate)
        return

@bot.command()
async def users_topics(ctx, *, in_text):
    user = in_text.replace("@!", "") #to remove the @ and ! sign from user pings
    out_string = ""
    for person in classmates:
        if person.name == user or "<" + str(person.id) + ">" == user: #id is returned in pings rather than the name dispite appearing as the name
            if len(person.topics) <= 0:
                await ctx.send("User has any topics currently")
            for topic in person.topics:
                out_string = out_string + topic + ", "
            out_string = out_string[:-2]
            await ctx.send(out_string)
            return
    await ctx.send("User has not added any topics or does not exist")

@bot.command()
async def my_topics(ctx):
    out_string = ""
    for person in classmates:
        if person.id == ctx.message.author.id:
            if len(person.topics) <= 0:
                await ctx.send("You currently do not have any Leetcode Topics Set")
                return
            for topic in person.topics:
                out_string = out_string + topic + ", "
            out_string = out_string[:-2]
            await ctx.send(out_string)
            return
    await ctx.send("You do not have any LeetCode Topics set yet")

@bot.command()
async def topics_clear(ctx):
    for person in classmates:
        if person.id == ctx.message.author.id:
            person.topics = []

@bot.command()
async def topics_remove(ctx, *, in_text):
    topicsToRemove = in_text.split(", ")
    for person in classmates:
        if person.id == ctx.message.author.id:
            for toRemove in topicsToRemove:
                person.topics.remove(toRemove)

@bot.command()
async def topic_find(ctx, *, in_text):
    matches = []
    out_string = ""
    for person in classmates:
        if in_text in person.topics:
            matches.append(person.name)
    if len(matches) <= 0:
        await ctx.send("No matches found.")
        return
    for match in matches:
        out_string = out_string + match + ", "
        out_string = out_string[:-2]
    await ctx.send(out_string)

@bot.command()
async def shared_topics(ctx):
    matches = []
    out_string = ""
    for person in classmates:
        if person.id == ctx.message.author.id:
            user = person
    for person in classmates:
        if user.id != person.id and not set(person.topics).isdisjoint(user.topics):
            matches.append(person.name)
    if len(matches) <= 0:
        await ctx.send("No matches found.")
        return
    for match in matches:
        out_string = out_string + match + ", "
        out_string = out_string[:-2]
    await ctx.send(out_string)


    





bot.run(TOKEN)
#bot.run(TOKEN.read())
