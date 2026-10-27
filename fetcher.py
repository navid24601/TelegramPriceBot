# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 01:00:00 2026

@author: Navid
"""

import requests  # For fetching the webpage
from bs4 import BeautifulSoup  # For parsing HTML
import re  # For pattern matching in text
import asyncio  # For async waiting (non-blocking)
from database import save_price, get_latest_price, get_all_users  # Import database functions
from bot import bot  # Import the bot to send messages (we'll create bot.py next)

URL = "https://noghresea.ir/silver-price"  # The webpage to fetch

def fetch_price():
    """Fetch and parse the latest price from the website."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(URL, headers=headers)  # Add proxies=... if needed
    try:
        response = requests.get(URL)  # Get the page content
        # If filtered, add proxies: response = requests.get(URL, proxies={'http': 'socks5://localhost:1080'})
        response.raise_for_status()  # Check for errors
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse HTML
        text = soup.get_text()  # Get all text from the page
        
        # Find price and timestamp using patterns (adjust if site changes)
        price_match = re.search(r'قیمت الان:\s*([\d,]+)\s*تومان', text)  # Matches "قیمت الان: 550,930 تومان"
        # Alternative if above fails: price_match = re.search(r'نرخ فعلی\s*:\s*([\d,]+)\s*تومان', text)
        timestamp_match = re.search(r'([۰-۹]+\s*\w+\s*\d{4}\s*-\s*[۰-۹]+:[۰-۹]+:[۰-۹]+)', text)  # Matches Persian "۰۵ اسفند ۱۴۰۴ - ۰۶:۰۳:۵۶"
        
        if price_match and timestamp_match:
            price_str = price_match.group(1).replace(',', '')  # Remove commas, e.g., "541,390" -> "541390"
            price = int(price_str)  # Convert to number
            timestamp = timestamp_match.group(1)
            return timestamp, price
    except Exception as e:
        print(f"Error fetching price: {e}")  # Log errors for debugging
    return None, None

async def poll_and_check():
    """Background loop: Check website every 60 seconds, save new prices, and send alerts."""
    last_price = None
    while True:  # Run forever
        timestamp, price = fetch_price()
        if price and price != last_price:  # Only save/send if price changed
            save_price(timestamp, price)
            last_price = price
            # Check all users for alerts
            users = get_all_users()
            for chat_id, high, low in users:
                if high and price >= high:
                    await bot.send_message(chat_id, f"Alert: Price reached high threshold! Current: {price} Tomans")
                if low and price <= low:
                    await bot.send_message(chat_id, f"Alert: Price reached low threshold! Current: {price} Tomans")
        await asyncio.sleep(60)  # Wait 1 minute before checking again
        
