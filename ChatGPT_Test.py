import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime

# HM-10 蓝牙设备的地址和特征值 UUID
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
HM10_ADDRESS = "68:5E:1C:2B:75:8E"  # 替换成你的设备地址！

# 存储蓝牙返回数据
def handle_notify(sender, data):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 📥 Arduino 发送: {data.decode(errors='ignore')}")

async def main():
    print("🔍 正在搜索设备...")
    devices = await BleakScanner.discover()
    found = False
    for d in devices:
        print(f"🔎 找到设备: {d.name} - {d.address}")
        if d.address.lower() == HM10_ADDRESS.lower():
            found = True

    if not found:
        print("❌ 没有找到指定设备，请确认地址正确或设备已开启。")
        return

    print(f"🔗 尝试连接 {HM10_ADDRESS} ...")
    async with BleakClient(HM10_ADDRESS) as client:
        print("✅ 已连接 HM-10！")

        # 启用通知
        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)

        try:
            while True:
                msg = input("💬 发送内容（输入 exit 退出）：")
                if msg.lower() == "exit":
                    break
                await client.write_gatt_char(CHARACTERISTIC_UUID, msg.encode())
                await asyncio.sleep(0.1)  # 等待稳定通信
        except KeyboardInterrupt:
            print("\n🛑 手动中断" )

        await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(main())
