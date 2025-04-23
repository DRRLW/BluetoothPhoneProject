import asyncio
from bleak import BleakScanner

async def main():
    print("🔍 正在扫描附近的 BLE 设备...")
    devices = await BleakScanner.discover(timeout=10.0)
    for i, d in enumerate(devices):
        print(f"{i+1}. 名称: {d.name}, 地址: {d.address}")

asyncio.run(main())
