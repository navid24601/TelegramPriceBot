# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 01:01:17 2026

@author: Navid
"""

import asyncio  # For running async tasks
from fetcher import poll_and_check  # Import the poller
from bot import bot, dp  # Import bot and dp

async def main():
    """Start the price poller in the background, then run the bot."""
    asyncio.create_task(poll_and_check())  # Run polling async
    await dp.start_polling(bot, skip_updates=True)  # Start listening for messages (v3 style)

if __name__ == '__main__':
    asyncio.run(main())  # Run the main function