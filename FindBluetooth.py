import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for BLE devices..")
    devices = await BleakScanner.discover(timeout=10.0)
    for i, d in enumerate(devices):
        print(f"{i+1}. Name: {d.name}, MAC Address: {d.address}")

asyncio.run(main())
