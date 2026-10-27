# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 00:59:27 2026

@author: Navid
"""

import sqlite3  # Built-in library for a simple database

# Connect to (or create) the database file
conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS prices 
                  (timestamp TEXT, price INTEGER)''')  # Stores price history
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (chat_id INTEGER PRIMARY KEY, high_alert INTEGER, low_alert INTEGER)''')  # Stores user alerts
conn.commit()  # Save changes

def save_price(timestamp, price):
    """Save a new price to the database."""
    cursor.execute("INSERT INTO prices (timestamp, price) VALUES (?, ?)", (timestamp, price))
    conn.commit()

def get_latest_price():
    """Get the most recent price."""
    cursor.execute("SELECT price FROM prices ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None  # Return None if no data yet

def set_user_alerts(chat_id, high, low):
    """Set or update alerts for a user."""
    cursor.execute("INSERT OR REPLACE INTO users (chat_id, high_alert, low_alert) VALUES (?, ?, ?)", (chat_id, high, low))
    conn.commit()

def get_all_users():
    """Get all users and their alerts to check."""
    cursor.execute("SELECT chat_id, high_alert, low_alert FROM users")
    return cursor.fetchall()