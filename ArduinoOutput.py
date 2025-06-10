import serial
import wave
import struct
import time

# 配置参数
PORT = 'COM3'         # 根据实际情况修改端口
BAUD_RATE = 9600
SAMPLE_RATE = 8000     # Hz
DURATION_SECONDS = 25  # 录音时长

# 初始化串口
ser = serial.Serial(PORT, BAUD_RATE)
time.sleep(2)  # 等待 Arduino 启动

samples = []
start_time = time.time()

print("开始接收数据...")

while len(samples) < SAMPLE_RATE * DURATION_SECONDS:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print("收到数据：", line)  # Debug 打印串口数据

        if line.startswith("SAMPLE"):
            parts = line.split(',')
            if len(parts) >= 4:
                mic_value = int(parts[2])
                # 将0~1023映射到 -32768~32767（16-bit PCM）
                pcm_val = int((mic_value - 512) * (32767 / 512))
                # 限制范围，防止超出short格式
                pcm_val = max(-32768, min(32767, pcm_val))
                #pcm_val = int((mic_value - 512) / 512 * 32767)
                samples.append(pcm_val)
    except Exception as e:
        print("解析错误：", e)

    # 防止死循环：如果超过 10 秒还没接满数据就强制跳出
    if time.time() - start_time > DURATION_SECONDS + 5:
        print("超时退出，未接收到足够数据。")
        break

ser.close()

if len(samples) == 0:
    print("没有接收到任何有效数据，退出。")
    exit()

print(f"接收完成，共接收 {len(samples)} 个样本，开始写入 WAV 文件...")

# 写入 WAV 文件
with wave.open('output.wav', 'w') as wf:
    wf.setnchannels(1)          # 单声道
    wf.setsampwidth(2)          # 2字节 = 16-bit
    wf.setframerate(SAMPLE_RATE)
    for s in samples:
        wf.writeframes(struct.pack('<h', s))  # 写入16-bit小端格式

print("写入完成！output.wav 保存成功")
