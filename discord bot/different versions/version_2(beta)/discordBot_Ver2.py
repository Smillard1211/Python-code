from ctypes.wintypes import PFILETIME
from email.headerregistry import ParameterizedMIMEHeader
from shutil import move

import string
from typing_extensions import Self
import discord
from discord.ext import tasks, commands
from discord import Color as c
from discord import guild
import random
import time
import csv
import os
import asyncio
from discord.utils import get
from discord.ext.commands.core import _CaseInsensitiveDict
from discord.utils import sleep_until

global dict
global annoyC
global count
global highChance
count = int(0)
dict = {555: 0}
annoyC = {}
highChance = {}
global maxMove
maxMove = 75

global task
global testUser
testUser = None
global gamePlayer
gamePlayer = []
global player
player = []
global playerA
playerA = []
global Pmove
Pmove = {}
global Pmoney
Pmoney = {}
global Pitem
Pitem = {}
global prizePool
prizePool = {"prize" : 0}
global currPlayer
currPlayer = 0
global start
start = False
global nameList
nameList = []




#=====================================================================    helper methods
def updateFile():
	os.remove("Score.txt")

	with open("Score.txt", "w", newline='') as test:
		test.write('person money\n')
		for key, value in dict.items():
			enter = str(key) + ' ' + str(value) + '\n'

			test.write(enter)


#used for multiple of shop items(list = dictionary used, name = .txt file)
def updateStuff(name, list):
	os.remove(name)

	with open(name, "w", newline='') as here:
		here.write('person value\n')
		for key, value in list.items():
			enter = str(key) + ' ' + str(value) + '\n'

			here.write(enter)

#uploads the text file to be a dict in the code(list = dict used, name = .txt file)
def uploadDict(name, list):
    with open(name, newline='') as score:
         score_reader = csv.DictReader(score, delimiter = ' ')
         for score in score_reader:
              list.update({int(score['person']): int(score['value'])})

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


def printList(r):
    tmp = "" 
    for x in r:
        tmp = tmp + x +  ", "
    
    return tmp


        
def steal(main, steal):
    print("work in progress")

def randomItem(player):
    print("work in progress")


def prizeTime(player, prize):
    print('work in progress')

#==================================================================start functions

with open("Score.txt", newline='') as score:
	score_reader = csv.DictReader(score, delimiter=' ')
	for score in score_reader:

		dict.update({int(score['person']): int(score['money'])})
          

uploadDict("higher.txt", highChance)



#==================================================================Bot start with the cogs


class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=['$'])

        self.add_cog(main(self)) #the class that are for basic commands
        self.add_cog(game(self)) #the class that holds the board game
        

        intents = discord.Intents.default()
        intents.members = True
        intents=intents

    async def on_ready(self):
       
        print(f'Logged in as {self.user.name} | {self.user.id}')

class game(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
    
 #============================================================================================================================The commands
    @commands.command()
   
    async def joinGame(self,ctx):
        gamePlayer.append(ctx.author)#used for the message.author bit 
        await ctx.send("you are player {}".format(len(player)+1))
        player.append(ctx.author.id)#id of the player
        print(player)
        nameList.append(ctx.author.name)#name of the user
        tmp = ctx.author.name
        Pmove.update({tmp: 0})
        Pmoney.update({tmp: 50})
        Pitem.update({tmp:['skip', 'skip', 'skip']})
        global prizePool
        #the final prize pool of the players(add when the testing phase is done)
        #prizePool.update({"prize" : (prizePool.get("prize") + int(arg))})
        #print(prizePool.get("prize"))
        if (len(gamePlayer) == 5):
            await ctx.invoke(self.bot.get_command('gameStart'))
        
    @commands.command()
    async def gameStart(self,ctx):
        if (len(player) < 2):
            await ctx.send('Needs at least 2 players')
            return
        else:
            await ctx.send('gambling may not be avaliable until the game is done or enough people force quit(Not working yet, just ask the creator to quit)\n\n\n')
            await ctx.send('------------------HOW TO PLAY------------------ \n\n Since discord is dumb I have had to change how the game works \n\n Basically to play you would need to type ".round" when it is your turn\n- Also type in an anwser(When prompted) with no "$" if asked for something')
            global start 
            start = True 
            
            
            
                #pain begins
    @commands.command()
    async def round(self, ctx):            
            if start == False:
                return

            else:
                global currPlayer
                user = gamePlayer[currPlayer]
                test = player[currPlayer]

                if ctx.author.id != test:
                    return

                tmp = nameList[currPlayer]
                move = Pmove.get(tmp)
                money = Pmoney.get(tmp)
                item = Pitem.get(tmp)
                        
                await ctx.send("{}'s turn".format(tmp))
                await ctx.send("choose what to do\n- roll(roll)\n- use an Item(use)\nAlso you have {}".format(money))
                msg = await self.bot.wait_for('message', check=lambda message: message.author == user)
                
                #main choice for the player
                if msg.content.lower() == "roll":
                    dice = random.randint(1, 10)
                    move = dice + int(move)
                    await ctx.send("you moved {}".format(dice))
                    await ctx.send("you are at {}".format(move))
                    #the spots part

                    if move >20:
                         print(test)


                                    
                    if move >= maxMove:
                        ctx.send("{} has won".format(ctx.user.name))
                        Pmoney.clear
                        Pmove.clear
                        nameList.clear
                        Pitem.clear
                        playerA.clear
                        gamePlayer.clear

                        return
                
                #the items to be used for the board game                      
                if msg.content.lower() == "use":
                        if len(item) == 0:
                            await ctx.send("you have no items get some you poor soul")
                        else:   
                            await ctx.send("your items are:" + printList(item))
                            await ctx.send("choice which one (they must be exactly the same)")
                            msg = await self.bot.wait_for('message', check=lambda message: message.author == user)
                            if msg.content.lower() == "skip" and item.count("skip") > 0:
                                await ctx.send("You skipped the next player")
                                item.remove("skip")
                                currPlayer += 1
                                if currPlayer >= int(len(gamePlayer)):
                                    currPlayer = 1
                                    await ctx.send("the next player is now{}".format(nameList[currPlayer]))
                                return
                            if msg.content.lower() == "money" and item.count("money") > 0:
                                await ctx.send("You gained 20 bucks")
                                item.remove("money")
                                money += 20
                                return
                            if msg.content.lower() == "random":
                                await ctx.send("how did you find this")


                Pmove.update({tmp:move})
                Pmoney.update({tmp:money})
                Pitem.update({tmp:item})
                currPlayer += 1
                
                if currPlayer >= int(len(gamePlayer)):
                    currPlayer = int(0)
                await ctx.send("next Player is {}".format(nameList[currPlayer]))
                        
                    
                        
    
    #very basic spot method to be used for later
    @commands.command()
    async def Spot(self, ctx, user, money, point, player):
        if(point == 1):
            ctx.send('nothing')
            return
        elif(point == 2):
            ctx.send('nothing')
            return
        elif(point == 3):
            print('bank')
            return

    #spot that will be used in the board game as a spot    
    @commands.command()
    async def bank(self, ctx, user, money):#must return the money value
        if(player.contains(user)) < 1:
            return
        else:
            await ctx.send("you have not payed your loan either pay(pay) the price or go to jail")
            msg = await self.bot.wait_for('message', check=lambda message: message.author == user)
            if msg.content.lower() == "pay":
                await ctx.send("*you gave 20 bucks to the bank*(they still want more though you know like a bank)")
                return 1
            else:
                await ctx.send("I see you submit time for jail")
                return 2

    @commands.command()
    async def court(self, ctx):
        print("work in progress")


#==============================================================================================================

#the main class that has the main functions            

#==============================================================================================================
class main(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    #makes the roles on the server if they do not already exist
    @commands.command()
    async def makeRoles(self, ctx):
        user = ctx.author.id
        if user == 210457357040353280:
            if get(ctx.guild.roles, name="Spender") == None:
                await ctx.guild.create_role(name="Spender", color=c.gold())     
                await ctx.send("role made") 

            if get(ctx.guild.roles, name="higherChance") == None:
                await ctx.guild.create_role(name="higherChance", color=c.magenta())

         
        
    #the main gamble command using fake money
    @commands.command()
    async def gamble(self, ctx, arg):
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

        role = discord.utils.get(ctx.guild.roles, name="HigherChance")
        if ((role in ctx.author.roles or ctx.author.id == ctx.guild.owner_id) and highChance.get(ctx.author.id) == 1):
            await ctx.send("High chance role")
            num = HigherMoney(int(arg))
            temp = int(price) - int(arg)
            if ctx.author.id == ctx.guild.owner_id:
                 highChance.update({ctx.author.id: 0})
            else:     
                await ctx.author.remove_roles(role)
                highChance.update({ctx.author.id: 0})
            addPrice = int(temp) + int(num)
        else:
            num = moneyTime(int(arg))
            temp = int(price) - int(arg)
            addPrice = int(temp) + int(num)

        #========================================
        if num == 0:
            dict.update({ctx.author.id: temp})
            num = int(dict.get(555))
            dict.update({555: int(num + int(arg))})
            await ctx.send("Lost {} Stale Coins".format(arg))

            updateFile()
        else:
            dict.update({ctx.author.id: addPrice})
            await ctx.send("Won {} Stale Coins".format(num))

            updateFile()

    #random chance to get a small amount of money 
    @commands.command()
    async def beg(self,ctx):
        num = 0
        if ctx.author.id == 210457357040353280:
            await ctx.send("of course I give money to you. Added 10000000000")
            price = int(dict.get(ctx.author.id) + 10000000000)
            dict.update({ctx.author.id: price})
            updateFile()
        else:    
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
            
    #shows the amount of money the user has
    @commands.command()
    async def rank(self,ctx):
        num = ctx.author.id
        if dict.get(num) == num:
             await ctx.send("you not real leave. Use '$gamble 20' to make account")
        else:
             await ctx.send("You have {} Stale Coins".format(dict.get(num)))
        
    #lets users give money to each other
    @commands.command()
    async def give(self, ctx, arg:discord.Member, arg2):
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
    
    #shows how much money the user has
    @commands.command()
    async def user(self, ctx, arg:discord.Member):
        if dict.get(arg.id) == None:
            dict.update({arg.id: int(100)})
            await ctx.send(
                "They Don't exist yet, they do now though(they have 100 Stale Coins)"
            )
        else:
            await ctx.send("That user has {} Stale Coins".format(dict.get(arg.id)))

    #shows the different items to be bought on te store
    @commands.command()
    async def store(self, ctx):
        await ctx.send(
	    'Spender - 1,000,000,000\nHigherChance - 1,000\nScream - 1,000(WIP)')

    #buys different roles that do specific things on the server
    @commands.command()
    async def buy(self, ctx, arg):
        user = ctx.author.id
        owner = ctx.guild.owner_id
        if arg.lower() == 'spender':
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
        if arg.lower() == 'higherchance':
            role = discord.utils.get(ctx.guild.roles, name="higherChance")
            if(user == ctx.guild.owner_id and highChance.get(user) == 1):
                 await ctx.send("use the chance already")
            
            elif(role in ctx.author.roles and highChance.get(user) == 1):
                await ctx.send("Use the chance already")
            elif int(dict.get(user)) < int(1000):
                await ctx.send("You don't have that much money")
            else:
                dict.update({user: int(dict.get(user) - 1000)})
                if(user == owner):
                    await ctx.send("can't give role but you do have it")
                    highChance.update({user: 1})
                    updateFile()
                    updateStuff("higher.txt", highChance)
                else:
                    await ctx.author.add_roles(role)
                    highChance.update({user: 1})
                    updateFile()
                    updateStuff("higher.txt", highChance)
                    await ctx.send('You have one chance for a higher gamble chance')

    #shows the collective loss for the whole bot
    @commands.command()
    async def gameBank(self, ctx):
        await ctx. send('there as been a colletive loss of {} stale coins'.format(dict.get(555)))

    #taxes every user can only be controlled by one user
    @commands.command()
    async def tax(self, ctx):
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
            updateFile()
        else:
            await ctx.send('No')

    @commands.command()
    async def backup(self, ctx):
        if ctx.author.id == 210457357040353280:
            backupFile()
            await ctx.send("Backup created")
            await ctx.send("bot may go down for a bit")
        else:
            return
            

    @commands.command()
    async def updateWeb(ctx):
        os.remove("website.txt")

        with open("website.txt", "w", newline='') as test:
            test.write('person money\n')
            for key, value in dict.items():
                if key == 555:
                    user = 'loss'
                elif key == 210457357040353280:
                    user = 'Mother'
                else:
                    user = await bot.fetch_user(key)
                    user = user.name
                enter = str(user) + ' ' + str(value) + '\n'

                test.write(enter)   
              
      
    @commands.command()
    async def ownerRole(self, ctx):
        user = ctx.author.id
        if user == ctx.guild.owner_id:
            await ctx.send("you have: ")
            if highChance.get(user) == 1:
                await ctx.send("HigherChance")
            print()

    @commands.command()
    async def storeInfo(self, ctx):
	    await ctx.send("Spender - A very good purposful role\nHigherChance - give one chance for a higher gamble chance")
    


bot = Bot()
bot.run('Token')