import asyncio
from bleak import BleakClient, BleakScanner

# HM-10 的 BLE UUID（多数设备都是这组）
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# 改成你自己的 HM-10 MAC 地址
ADDRESS = "68:5E:1C:2B:75:8E"

MAX_CHUNK_SIZE = 20  # HM-10 一次最多支持 20 字节

def handle_notify(_, data):
    print(f"\n📥 [收到字节] {data}")
    try:
        msg = data.decode('utf-8')
    except UnicodeDecodeError:
        msg = data.decode('utf-8', errors='replace')
    print(f"📥 [已解码] {msg}")

async def main():
    print("🔍 正在扫描设备...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"🔹 {d.name} - {d.address}")

    print(f"\n🔗 尝试连接到 {ADDRESS}...")
    async with BleakClient(ADDRESS) as client:
        print("✅ 已连接！")

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)

        while True:
            try:
                text = input("\n📝 发送消息（exit退出）: ")
            except UnicodeDecodeError:
                print("❌ 输入解码错误，请重新输入。")
                continue

            if text.lower() == "exit":
                break

            # 分段发送
            for i in range(0, len(text), MAX_CHUNK_SIZE):
                chunk = text[i:i+MAX_CHUNK_SIZE]
                await client.write_gatt_char(CHARACTERISTIC_UUID, chunk.encode())
                await asyncio.sleep(0.05)

        await client.stop_notify(CHARACTERISTIC_UUID)
        print("📴 已断开连接。")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n👋 已退出程序")
