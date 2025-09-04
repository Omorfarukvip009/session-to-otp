# login.py
import sys
import re
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession

if len(sys.argv) < 4:
    print("Usage: python login.py <API_ID> <API_HASH> <SESSION_FILE>")
    sys.exit(1)

API_ID = int(sys.argv[1])
API_HASH = sys.argv[2]
SESSION_FILE = sys.argv[3]

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

client.connect()
if client.is_user_authorized():
    print("✅ User Authorized!")

    @client.on(events.NewMessage(from_users=777000))
    async def get_otp_msg(event):
        otp = re.search(r'\b(\d{5})\b', event.raw_text)
        if otp:
            print(f"OTP received: {otp.group(0)}")
            client.disconnect()
            sys.exit(0)

    with client:
        client.run_until_disconnected()
else:
    print("🔴 Authorization Failed!")
    sys.exit(1)
  
