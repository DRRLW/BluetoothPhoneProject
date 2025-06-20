import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
ADDRESS = "68:5E:1C:2B:75:8E"
MAX_CHUNK_SIZE = 20

reply_event = asyncio.Event()
buffer = ""

def handle_notify(_, data):
    global buffer
    try:
        chunk = data.decode('utf-8')
    except UnicodeDecodeError:
        chunk = data.decode('utf-8', errors='replace')
    print(f"\n[Chunk] {chunk}")
    buffer += chunk
    if buffer.endswith("\n"):
        print(f"[Full message] {buffer.strip()}")
        reply_event.set()

async def main():
    print("Scanning available devices")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f" {d.name} - {d.address}")

    print(f"\nAttempting to connect {ADDRESS}...")
    async with BleakClient(ADDRESS) as client:
        print("Connected")

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)

        while True:
            try:
                text = input("\nSending (type exit to leave): ")
            except UnicodeDecodeError:
                print("Decoding error, please enter again")
                continue

            if text.lower() == "exit":
                break

            global buffer
            buffer = ""
            reply_event.clear()

            for i in range(0, len(text), MAX_CHUNK_SIZE):
                chunk = text[i:i+MAX_CHUNK_SIZE]
                await client.write_gatt_char(CHARACTERISTIC_UUID, chunk.encode())
                await asyncio.sleep(0.05)
            await client.write_gatt_char(CHARACTERISTIC_UUID, b"\n")

            print("Waiting for response...")
            try:
                await asyncio.wait_for(reply_event.wait(), timeout=30.0)
            except asyncio.TimeoutError:
                print("Timeout: no complete response received")

        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Disconnected")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nProgram ended")
