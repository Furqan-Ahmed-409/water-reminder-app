# import time
# from plyer import notification
#
#
# while True:
#     print("Please sip some water")
#     notification.notify(title="WATER REMINDER",
#                         message="You have to drink some water",
#                         timeout=10)
#     time.sleep(60*60)

'''
Free Water Reminder System Tutorial
Send water drinking alerts to your phone 24/7 - completely free!
🎯 What You'll Build
A Python bot that runs in the cloud and sends water drinking reminders to your Telegram app every hour (or custom interval) - even when your computer is off.
📋 Prerequisites

Telegram app on your phone
Basic Python knowledge
Git installed on your computer
GitHub account
Railway account (free)


Step 1: Create Your Telegram Bot
1.1 Install Telegram

Download Telegram on your phone from App Store/Play Store
Create an account if you don't have one

1.2 Create the Bot

Open Telegram and search for @BotFather
Start a chat with BotFather
Send /newbot command
Choose a name for your bot (e.g., "My Water Reminder")
Choose a username ending with "bot" (e.g., "mywater_reminder_bot")
Save the Bot Token - you'll need this later (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)

1.3 Get Your Chat ID

Send a message to your new bot
Open this URL in browser: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
Look for "chat":{"id": and copy the number (your Chat ID)
Save your Chat ID (looks like: 123456789)


Step 2: Create the Python Application
2.1 Create Project Structure
Create a new folder for your project:
water-reminder/
├── main.py
├── requirements.txt
├── runtime.txt
└── README.md
'''
# Import libraries we need for our water reminder bot
import os  # To read environment variables (secret settings)
import time  # To add delays and pauses
import requests  # To send messages to Telegram servers
import schedule  # To schedule reminders at specific times
from datetime import datetime  # To get current time
import threading  # For running multiple tasks (not used in this simple version)

# 📝 STEP 1: Get our secret settings from environment variables
# These are stored securely on the hosting platform, not in our code
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # Our bot's secret password
CHAT_ID = os.environ.get('CHAT_ID')  # Our personal chat ID number
REMINDER_INTERVAL = int(os.environ.get('REMINDER_INTERVAL', 60))  # How often to remind (default: 60 minutes)


class WaterReminderBot:
    """
    This is our main bot class - think of it as a blueprint for our water reminder robot
    It contains all the instructions our bot needs to work
    """

    def __init__(self, bot_token, chat_id):
        """
        This function runs when we create a new bot
        It's like giving our bot its identity and contact information
        """
        self.bot_token = bot_token  # Store the bot's secret password
        self.chat_id = chat_id  # Store our chat ID (where to send messages)
        # Create the URL we'll use to talk to Telegram servers
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, message):
        """
        This function sends a message to our phone via Telegram
        Think of it as our bot's mouth - how it talks to us
        """
        # Create the web address where we send our message
        url = f"{self.base_url}/sendMessage"

        # Prepare the message data to send
        data = {
            'chat_id': self.chat_id,  # Where to send (our phone)
            'text': message,  # What to send (the reminder text)
            'parse_mode': 'HTML'  # Allow bold/italic text formatting
        }

        # Try to send the message (with error handling)
        try:
            # Send HTTP request to Telegram servers
            response = requests.post(url, data=data)

            # Check if message was sent successfully
            if response.status_code == 200:
                print(f"✅ Message sent: {message}")
            else:
                print(f"❌ Failed to send message: {response.text}")

        except Exception as e:
            # If something goes wrong, print the error
            print(f"❌ Error sending message: {e}")

    def send_water_reminder(self):
        """
        This function creates and sends a water drinking reminder
        It picks a random message to keep things interesting
        """
        # List of different reminder messages (you can add more!)
        messages = [
            "💧 Time to drink water! Stay hydrated! 🚰",
            "🌊 Hydration check! Drink a glass of water now! 💙",
            "💦 Your body needs water! Take a sip! 🥤",
            "🚰 Water break time! Keep yourself healthy! 💧",
            "💙 Reminder: Drink water for better health! 🌊"
        ]

        # Import random module to pick a random message
        import random
        message = random.choice(messages)  # Pick one message randomly

        # Get current time and format it nicely (like "14:30")
        current_time = datetime.now().strftime("%H:%M")

        # Create the final message with time and reminder
        full_message = f"⏰ <b>{current_time}</b>\n{message}"

        # Send the message to our phone
        self.send_message(full_message)

    def start_reminders(self):
        """
        This is the heart of our bot - it starts the reminder system
        It sets up the schedule and keeps the bot running 24/7
        """
        # Print startup messages so we know the bot is working
        print(f"🚀 Water reminder bot started!")
        print(f"⏱️ Reminder interval: {REMINDER_INTERVAL} minutes")

        # 📅 SCHEDULE SETUP: Tell the bot when to send reminders
        # This line says: "Every X minutes, run the send_water_reminder function"
        schedule.every(REMINDER_INTERVAL).minutes.do(self.send_water_reminder)

        # Send a welcome message to our phone
        welcome_message = (
            "🎉 <b>Water Reminder Bot Activated!</b>\n"
            f"💧 You'll receive reminders every {REMINDER_INTERVAL} minutes.\n\n"
            "🔧 Commands:\n"
            "• Send 'stop' to pause\n"
            "• Send 'start' to resume"
        )
        self.send_message(welcome_message)

        # 🔄 MAIN LOOP: Keep the bot running forever
        # This is like the bot's heartbeat - it never stops checking for scheduled tasks
        while True:
            # Check if any scheduled reminders are due
            schedule.run_pending()
            # Wait 1 second before checking again (saves computer resources)
            time.sleep(1)

    def handle_commands(self):
        """
        Future feature: This could handle user commands like /start, /stop
        For now, it's just a placeholder for more advanced features
        """
        # This is a simple version - for full command handling, you'd need webhooks
        pass


def main():
    """
    This is the main function - the starting point of our program
    Think of it as the "power button" for our water reminder bot
    """

    # 🔍 SAFETY CHECK: Make sure we have the required settings
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Error: BOT_TOKEN and CHAT_ID environment variables are required!")
        print("💡 Make sure you've set up these variables in Railway/Heroku")
        return  # Stop the program if settings are missing

    # 🤖 CREATE THE BOT: Make a new WaterReminderBot with our settings
    bot = WaterReminderBot(BOT_TOKEN, CHAT_ID)

    # 🚀 START THE BOT: Begin sending reminders
    try:
        bot.start_reminders()  # This will run forever (until we stop it)

    except KeyboardInterrupt:
        # If someone presses Ctrl+C to stop the bot
        print("\n🛑 Bot stopped by user")

    except Exception as e:
        # If any other error happens, print it
        print(f"❌ Error: {e}")


# 🏁 PROGRAM ENTRY POINT
# This special line means "start here when the program runs"
if __name__ == "__main__":
    main()  # Run the main function

"""
📚 BEGINNER'S SUMMARY:

This program works like this:
1. Gets secret settings (bot token, chat ID, reminder interval)
2. Creates a WaterReminderBot object with those settings
3. Sets up a schedule to send reminders every X minutes
4. Runs forever, checking every second if it's time to send a reminder
5. When it's time, picks a random water reminder message
6. Sends that message to your phone via Telegram

Key concepts used:
- Classes: Like blueprints for creating objects (our bot)
- Functions: Reusable pieces of code that do specific tasks
- Loops: Code that repeats (while True = repeat forever)
- Error handling: try/except blocks to handle problems gracefully
- Environment variables: Secure way to store passwords and settings

The bot runs in the cloud 24/7, so you get reminders even when
your personal computer is turned off!
"""