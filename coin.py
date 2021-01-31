import asyncio, discord, random
from discord.ext import commands

token="???"
game = discord.Game("한강물 온도체크")
bot=commands.Bot(command_prefix="!", status=discord.Status.online, activity=game)
channel="???"
maindict={}
names=[]

async def change():
    global maindict
    global names
    namelst=open("hcoin_namelist.txt", "r")
    names=namelst.readlines()
    indx=0
    for name in names:
        names[indx]=name[:len(name)-1]
        indx+=1
    spltlst=[]
    main=open("hcoin.txt", "r")
    lst=main.readlines()
    main.close()
    indx=0
    for member in lst:
        lst[indx]=member[0:len(member)-1]
        spltlst.append(member)
        indx+=1
    indx=0
    for member in lst:
        lst[indx]=member.split("=")
        indx+=1
    maindict=dict(lst)
    namelst.close()
    main.close()
    await updatefile()
    
@bot.event
async def on_ready():
    main=open("hcoin.txt", "r+")
    namelst=open("hcoin_namelist.txt", "r+")
    main.close()
    namelst.close()
    print("ready")
    await change()

async def updatefile():
    global maindict
    mainlst=[]
    main=open("hcoin.txt", "w")
    for key in maindict:
        mainlst.append(str(key)+"="+str(maindict[key])+"\n")
    main.writelines(mainlst)
    main.close()

def isint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def ntm(member):
    return str(member.name)+"#"+str(member.discriminator)

def trimname(member):
    return str(member)[0:len(str(member))-5]

@bot.command()
async def 개설(ctx):
    global names
    namelst=open("hcoin_namelist.txt", "r")
    names=namelst.readlines()
    namelst.close()
    main=open("hcoin.txt", "a+")
    namelst=open("hcoin_namelist.txt", "a+")
    member=ntm(ctx.message.author)
    if not(str(member)+"\n" in names):
        main.write(str(member)+"="+"0\n")
        main.close()
        namelst.write(str(member)+"\n")
        namelst.close()
        await ctx.channel.send(str(member)[0:len(str(member))-5]+"님의 계좌가 개설되었습니다. 환영합니다.")
        await change()
    else:
        await ctx.channel.send(str(member)[0:len(str(member))-5]+" 님은 이미 통장이 존재합니다.")

@bot.command(pass_context=True)
async def 송금(ctx):
    global maindict
    global names
    namelst=open("hcoin_namelist.txt", "r")
    sendmoney=(str(ctx.message.content).split(" "))
    for i in sendmoney:
        if isint(i):
            sendmoney=int(i)
            break
    if isint(sendmoney):
        for member in ctx.message.mentions:
            if ntm(member) in names:
                if sendmoney>=0:
                    if int(maindict[ntm(ctx.message.author)])>=sendmoney:
                        maindict[ntm(ctx.message.author)]=int(maindict[ntm(ctx.message.author)])-sendmoney
                        maindict[ntm(member)]=int(maindict[ntm(member)])+sendmoney
                        await ctx.channel.send(str(member)[0:len(str(member))-5]+"님께의 송금이 완료되었습니다!")
                        await updatefile()
                    else:
                        await ctx.channel.send("잔고가 부족하여 "+str(member)[0:len(str(member))-5]+"님께의 송금이 취소되었습니다.")
                else:
                    await ctx.channel.send("삐용삐용 도둑이다아")
            else:
                await ctx.channel.send(str(member)[0:len(str(member))-5]+"님의 통장이 존재하지 않습니다.")
    else:
        await ctx.channel.send("자연수값의 코인을 송금해주세요!")
    namelst.close()

@bot.command()
async def 통장(ctx):
    await ctx.send(str(ntm(ctx.message.author))[0:len(str(ntm(ctx.message.author)))-5]+"님의 잔고는 "+str(maindict[ntm(ctx.message.author)])+"코인 입니다.")
              
bot.run(token)
