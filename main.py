import pexpect
import time
import math
import configparser
from discord.ext import commands

bot = commands.Bot(command_prefix='mc ')
timer = time.time()
config = configparser.ConfigParser()
config.read('secrets.ini')


def check_server_running():
    try:
        return child.isalive()
    except NameError:
        return False


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def start(ctx):
    if check_server_running():
        await ctx.send('Server is already running!')
    else:
        # start mc server
        global child
        child = pexpect.spawn(config['secrets']['start_script'], encoding='utf-8')

        # reset timer
        global timer
        timer = time.time()

        await ctx.send('Starting... This might take a while')
        child.expect('Unloading dimension', timeout=120)
        await ctx.send('Running!')


@bot.command()
async def stop(ctx):
    if check_server_running():
        countdown = math.ceil(100 - (time.time() - timer))
        if countdown <= 0:
            await ctx.send('Sending stop command...')
            child.sendline('stop')
            time.sleep(2)
            child.kill(1)
            await ctx.send(f'{"Not Clean!" if child.isalive() else "Clean Exit!"}')
        else:
            await ctx.send(f'You must wait {countdown}s before doing that!')
    else:
        await ctx.send('Server not is running!')


bot.run(config['secrets']['token'])