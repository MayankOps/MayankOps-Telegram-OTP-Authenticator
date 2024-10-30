import random
import telebot
from datetime import datetime

# Replace with your bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)
otp_store = {}

# Log file name
log_file = "otp_log.txt"

def generate_otp():
    return random.randint(100000, 999999)

def send_otp(user_id):
    otp = generate_otp()
    otp_store[user_id] = otp
    bot.send_message(user_id, f"Your OTP is: {otp}")
    print(f"OTP sent to user ID {user_id}.")
    log_otp(user_id, otp, "Sent")  # Log the OTP sent
    return otp

def verify_otp(user_id, entered_otp):
    if otp_store.get(user_id) == entered_otp:
        print("OTP verification successful!")
        log_otp(user_id, entered_otp, "Verified")  # Log the OTP verified
        del otp_store[user_id]  # Clear OTP after verification
        return True
    else:
        print("Invalid OTP. Please try again.")
        return False

def log_otp(user_id, otp, action):
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Log the details to a file
    with open(log_file, "a") as f:
        f.write(f"{user_id} - {otp} - {action} - {timestamp}\n")
        
        # If the action is "Verified", add a blank line afterwards for separation
        if action == "Verified":
            f.write("\n")

def main():
    user_id = input("Enter Telegram User ID: ")
    try:
        user_id = int(user_id)
        # Send OTP
        otp = send_otp(user_id)

        # Prompt user to enter OTP for verification
        entered_otp = int(input("Enter the OTP received: "))
        
        # Verify OTP
        if verify_otp(user_id, entered_otp):
            print("Access granted.")
            bot.send_message(user_id, "Access Granted")
        else:
            print("Access denied. Incorrect OTP.")
    except ValueError:
        print("Invalid User ID or OTP format. Please enter numeric values.")

if __name__ == '__main__':
    main()