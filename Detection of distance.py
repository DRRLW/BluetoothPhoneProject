import serial
import time
import pyttsx3

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)
engine.setProperty('rate', 170)

last_play_time = 0
play_cooldown = 10  # 播放间隔10秒，避免连续重复

def welcome_speech():
    text = "Hiya!do you want to come closer and talk to me?"
    engine.say(text)
    engine.runAndWait()

def main():
    global last_play_time
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"已连接串口 {SERIAL_PORT}")

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line == "DETECTED":
                now = time.time()
                if now - last_play_time > play_cooldown:
                    print("检测到人，播放欢迎语音")
                    welcome_speech()
                    last_play_time = now

            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"串口连接失败: {e}")
    except KeyboardInterrupt:
        print("程序终止")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
