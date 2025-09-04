import asyncio, sys, re
from telethon import TelegramClient, events, errors

if len(sys.argv) < 4:
    print("Usage: python login.py <API_ID> <API_HASH> <SESSION_FILE>")
    sys.exit(1)

API_ID = int(sys.argv[1])
API_HASH = sys.argv[2]
SESSION_FILE = sys.argv[3]

async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start()  # fully async, handles connect + authorization
    print("✅ User Authorized!")

    # Listen for Telegram OTP messages from 777000
    @client.on(events.NewMessage(from_users=777000))
    async def get_otp_msg(event):
        otp = re.search(r'\b(\d{5})\b', event.raw_text)
        if otp:
            print(f"OTP received: {otp.group(0)}")
            await client.disconnect()
            sys.exit(0)

    print("―― Waiting for OTP messages...")
    await client.run_until_disconnected()

try:
    asyncio.run(main())
except errors.RPCError as e:
    print(f"―― ❌ RPC error: {e}")
except Exception as e:
    print(f"―― ❌ Unexpected error: {e}")
    
