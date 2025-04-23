import asyncio
from bleak import BleakClient, BleakScanner

# HM-10 BLE UUID
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# HM-10 MAC Address
ADDRESS = "68:5E:1C:2B:75:8E"

MAX_CHUNK_SIZE = 20  # HM-10 only support up to 20 byte

def handle_notify(_, data):
    print(f"\n [received message] {data}")
    try:
        msg = data.decode('utf-8')
    except UnicodeDecodeError:
        msg = data.decode('utf-8', errors='replace')
    print(f" [decoded] {msg}")

async def main():
    print("Scanning for available devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"- {d.name} - {d.address}")

    print(f"\n Attempting to connect {ADDRESS}...")
    async with BleakClient(ADDRESS) as client:
        print("Successfully connected")

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)

        while True:
            try:
                text = input("\n Sending Message（type exit to leave）: ")
            except UnicodeDecodeError:
                print("Decoding error, please try again。")
                continue

            if text.lower() == "exit":
                break

            # Send by different packages
            for i in range(0, len(text), MAX_CHUNK_SIZE):
                chunk = text[i:i+MAX_CHUNK_SIZE]
                await client.write_gatt_char(CHARACTERISTIC_UUID, chunk.encode())
                await asyncio.sleep(0.05)

        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Disconnected")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n Leave the program")
