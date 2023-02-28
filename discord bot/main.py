#          *Disclaimer*
#bot should NOT be used with real money
#because it goes against Discord's TOS
import discord
from discord.ext import commands, tasks
from discord.ext.tasks import loop
import random
import time
import csv
import os
import asyncio

from keep_Alive import keep_alive
from keep_Alive import home

global dict
global annoyC
global testUser
global count
count = int(0)
testUser = None
dict = {555: 0}
annoyC = {}

with open("Score.txt", newline='') as score:
	score_reader = csv.DictReader(score, delimiter=' ')
	for score in score_reader:

		dict.update({int(score['person']): int(score['money'])})


#======================================helper methods
def updateFile():
	os.remove("Score.txt")

	with open("Score.txt", "w", newline='') as test:
		test.write('person money\n')
		for key, value in dict.items():
			enter = str(key) + ' ' + str(value) + '\n'

			test.write(enter)


#used for multiple of shop items(list = dictionary used, name = txt file)
def updateStuff(list, name):
	os.remove(name)

	with open(name, "w", newline='') as here:
		here.write('person value\n')
		for key, value in list.items():
			enter = str(key) + ' ' + str(value) + '\n'

			here.write(enter)


#method to backup of score.txt
def backupFile():
	os.remove("testing.txt")

	with open("testing.txt", "w", newline='') as test:
		test.write('person money\n')
		for key, value in dict.items():
			enter = str(key) + ' ' + str(value) + '\n'
			test.write(enter)


#higher chance in the gamble
def HigherMoney(price):
	test = random.random()
	if test >= .75:
		return price * 8
	elif test >= .5:
		return price * 4
	elif test >= .5:
		return price * 2
	elif test < .3:
		return 0


#normal chance of gamble
def moneyTime(price):
	test = random.random()
	if test >= .9:
		return price * 8
	elif test >= .75:
		return price * 4
	elif test >= .5:
		return price * 2
	elif test < .51:
		return 0


#========================================start the bot

client = discord.Client()

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():

	print("the bot is ready")


#========================================all of the commands


#command that does the gambling(non-real money)
@bot.command()
async def gamble(ctx, arg):
	if dict.get(ctx.author.id) == None:
		dict.update({ctx.author.id: int(100)})
		await ctx.send("you have been added")
		if int(arg) > dict.get(ctx.author.id):
			await ctx.send("You may think you have more, but you have 100")
			return
	if int(arg) < 0:
		await ctx.send("No, Just No")
		return
	if int(arg) == 0:
		ctx.send("but like why")
	price = dict.get(ctx.author.id)
	if int(arg) > int(price):
		await ctx.send(
		    "Ha Ha you poor. You don't have that much. You have {} Stale Coins"
		    .format(price))
		return

	#======================================

	role = discord.utils.get(ctx.guild.roles, id=941734296132153424)
	if role in ctx.author.roles:
		num = HigherMoney(int(arg))
		temp = int(price) - int(arg)
		await ctx.author.remove_roles(role)
		addPrice = int(temp) + int(num)
		print(addPrice)
	else:
		num = moneyTime(int(arg))
		temp = int(price) - int(arg)
		addPrice = int(temp) + int(num)

#========================================
	if num == 0:
		dict.update({ctx.author.id: temp})
		num = int(dict.get(555))
		dict.update({555: int(num + int(arg))})
		await ctx.send("Lost {} Stale Coinss".format(arg))

		updateFile()
	else:
		dict.update({ctx.author.id: addPrice})
		await ctx.send("Won {} Stale Coinss".format(num))

		updateFile()


#random chance to get 10 bucks from the bot
@bot.command()
async def beg(ctx, arg=int(1)):
	num = 0
	if dict.get(ctx.author.id) == None:
		dict.update({ctx.author.id: 100})
	num = random.random()
	if num >= .9:
		price = int(dict.get(ctx.author.id) + 10)
		dict.update({ctx.author.id: price})
		await ctx.send("fine here is 10 Stale Coins")
		updateFile()
	else:
		await ctx.send("yeah no I'm not giving money right now")


#shows the current amount of money that a person has
@bot.command()
async def rank(ctx):
	num = ctx.author.id
	if dict.get(num) == None:
		await ctx.send("you not real leave. Use '$gamble 20' to make account")
	else:
		await ctx.send("You have {} Stale Coins".format(dict.get(
		    ctx.author.id)))


#gives money from the user to a different user
@bot.command()
async def give(ctx, arg: discord.Member, arg2):
	if int(arg2) < 0:
		await ctx.send("No")
		return
	if dict.get(arg.id) == None:
		dict.update({arg.id: int(100)})
		await ctx.send("user you sent money to as been added")
	if dict.get(ctx.author.id) == None:
		dict.update({ctx.author.id: int(100)})
		await ctx.send("You have been added")
	if int(arg2) > dict.get(ctx.author.id):
		await ctx.send("you don't have that much money")
		return
	else:
		updateNum = int(dict.get(ctx.author.id)) - int(arg2)
		dict.update({ctx.author.id: updateNum})

		dict.update({arg.id: int(dict.get(arg.id) + int(arg2))})

		updateFile()
	await ctx.send("you have given {} Stale Coins".format(arg2))


#checks a diferent users coins and makes them a user with 100 coins if they are not in the system
@bot.command()
async def user(ctx, arg: discord.Member):
	if dict.get(arg.id) == None:
		dict.update({arg.id: int(100)})
		await ctx.send(
		    "They Don't exist yet, they do now though(they have 100 Stale Coins)"
		)
	else:
		await ctx.send("That user has {} Stale Coins".format(dict.get(arg.id)))


#A store to show the different items
@bot.command()
async def store(ctx):
	await ctx.send(
	    'Spender - 1,000,000,000\nSussy - 10,000\nHigherChance - 1,000\nScream - 1,000(WIP)'
	)


#command to buy the different items in the store
@bot.command()
async def buy(ctx, arg):
	user = ctx.author.id
	if arg == 'Spender':
		role = discord.utils.get(ctx.guild.roles, id=930535137748336690)
		if role in ctx.author.roles:
			await ctx.send("you already have that role")
		elif int(dict.get(user)) < int(1000000000):
			await ctx.send("You don't have that much money")
		else:
			dict.update({user: int(dict.get(user) - 1000000000)})
			await ctx.author.add_roles(role)
			updateFile()
			await ctx.send('why did you buy this')
#=====================================================
	if arg == 'Sussy':
		num = annoyC.get(user)
		role = discord.utils.get(ctx.guild.roles, id=930570164762705981)
		#if role in ctx.author.roles:
		if num == 1:
			await ctx.send("You are already among us sus")
			annoyC.update({ctx.author.id: 1})
			return
		elif int(dict.get(user)) < int(10000):
			await ctx.send("You don't have that much money")
			return

		dict.update({user: int(dict.get(user) - 10000)})
		annoyC.update({user: 1})
		await ctx.author.add_roles(role)
		updateFile()
		#updateStuff(annoyC, 'annoy.txt')
		await ctx.send('You are now sussy')
#=====================================================
	if arg == 'HigherChance':
		role = discord.utils.get(ctx.guild.roles, id=941734296132153424)
		if role in ctx.author.roles:
			await ctx.send("Use the chance already")
		elif int(dict.get(user)) < int(1000):
			await ctx.send("You don't have that much money")
		else:
			dict.update({user: int(dict.get(user) - 1000)})

			await ctx.author.add_roles(role)
			updateFile()
			await ctx.send('You have one chance for a higher gamble chance')


#===================================================


#shows the collective loss that has been done
@bot.command()
async def bank(ctx):
	await ctx.send('There as been a collective loss of {} Stale Coins'.format(
	    dict.get(555)))


#showing the different commands
@bot.command()
async def commands(ctx):
	await ctx.send(
	    'annoy - message someone 10 times\nbank - collective loss\nstore - a store\nbuy - buy from the store\ngive- takes in a users mention and a number\nuser - mention a user and get their rank\nrank - get your rank\ngamble - put in number and gamble\nwhy\nfunny\nbeg '
	)


@bot.command()  #taxing people takes 6% from everyone
async def tax(ctx):
	if ctx.author.id == 210457357040353280:
		keys = list(dict)
		num = int(1)
		while num != len(keys):
			dict.update({
			    keys[num]:
			    int(dict.get(keys[num]) - (dict.get(keys[num]) * .06))
			})
			if dict.get(keys[num]) < 0:
				dict.update({keys[num]: 0})
			num += 1
		await ctx.send('taxes have been taken')
		print(5)
		updateFile()
	else:
		await ctx.send('No')


#creates a backup of the current score sheet(mainly for when debugging)
@bot.command()
async def backup(ctx):
	if ctx.author.id == 210457357040353280:
		backupFile()
		await ctx.send("Backup created")
		await ctx.send("bot may go down for a bit")
	else:
		return


#shows info about the different store items
@bot.command()
async def storeInfo(ctx):
	await ctx.send(
	    "Sussy - Gives access to the annoy command\nSpender - A very good purposful role\nHigherChance - give one chance for a higher gamble chance"
	)


#WIP - works on making a file so a website can grab it and use it
@bot.command()
async def updateWeb(ctx):
	os.remove("website.txt")

	with open("website.txt", "w", newline='') as test:
		test.write('person money\n')
		for key, value in dict.items():
			if key == 555:
				print('here')
				user = 'loss'
			elif key == 210457357040353280:
				user = 'Father'
			else:
				user = await bot.fetch_user(key)
				user = user.name
			enter = str(user) + ' ' + str(value) + '\n'

			test.write(enter)


#does different actions based on different messages in chat, also makes sure that the bot is in the right chat
@bot.event
async def on_message(message):

	msg = message.content
	if message.author == bot.user:
		return

	if message.channel.id != 449748048734846976:
		return
	else:
		await bot.process_commands(message)


keep_alive()
bot.run('Token')
