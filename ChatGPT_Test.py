import asyncio
from bleak import BleakClient

ADDRESS = "68:5E:1C:2B:75:8E"  # 改成你的 MAC 地址
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# 分包函数，每包最多20字节
def split_message(msg, size=20):
    return [msg[i:i + size] for i in range(0, len(msg), size)]

async def main():
    async with BleakClient(ADDRESS) as client:
        print("✅ 连接成功")

        def handle_notify(_, data):
            print("📥 来自 Arduino: ", data.decode(errors="ignore"))

        await client.start_notify(CHAR_UUID, handle_notify)

        while True:
            text = input("📝 发送消息（exit退出）: ")
            if text.lower() == "exit":
                break

            chunks = split_message(text + "\n")  # 添加结束符
            for part in chunks:
                await client.write_gatt_char(CHAR_UUID, part.encode())
                await asyncio.sleep(0.1)

        await client.stop_notify(CHAR_UUID)

asyncio.run(main())
