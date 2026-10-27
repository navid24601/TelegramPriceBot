# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 01:00:54 2026

@author: Navid
"""

from aiogram import Bot, Dispatcher, types  # Core bot libraries
from aiogram.filters import Command  # For command filters
from database import get_latest_price, set_user_alerts  # Import database functions

BOT_TOKEN = 'bot_token_goes_here'  # Paste your token from Step 2 (keep secret!)

bot = Bot(token=BOT_TOKEN)  # Create the bot
dp = Dispatcher()  # Dispatcher handles messages

@dp.message(Command(commands=['start']))
async def start(message: types.Message):
    """Welcome message when user starts the bot."""
    await message.reply("Welcome! Use /price for latest price, /setalert <high> <low> to set alerts (e.g., /setalert 600000 500000). Use 0 to disable.")

@dp.message(Command(commands=['price']))
async def price(message: types.Message):
    """Send the latest price to the user."""
    latest = get_latest_price()
    if latest:
        await message.reply(f"Latest silver price: {latest} Tomans")
    else:
        await message.reply("No price data yet. Checking soon!")

@dp.message(Command(commands=['setalert']))
async def set_alert(message: types.Message):
    """Set high/low alerts based on user input."""
    args = message.text.split()[1:]  # Get arguments after the command (manual split in v3)
    if len(args) == 2:
        high = int(args[0]) if args[0] != '0' else None
        low = int(args[1]) if args[1] != '0' else None
        set_user_alerts(message.chat.id, high, low)
        await message.reply(f"Alerts set: High={high or 'disabled'}, Low={low or 'disabled'}")
    else:
        await message.reply("Usage: /setalert <high> <low>")