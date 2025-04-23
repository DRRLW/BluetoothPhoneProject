
import openai
import speech_recognition as sr
import pyttsx3
import time

# 初始化语音合成引擎
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)
engine.setProperty('rate', 170)


def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...（停顿结束识别）")
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 1.5
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        print("正在识别...")
        text = recognizer.recognize_google(audio, language='en-UK')
        print("你说的是：", text)
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
        return None
    except sr.RequestError as e:
        print("识别服务出错；{0}".format(e))
        return None


def text_to_speech(text):
    if text:
        print(f"开始朗读：{text}")
        engine.say(text)  # 语音合成
        engine.runAndWait()  # 等待语音播放完成
    else:
        print("没有要朗读的内容")


# 模拟按钮状态（False 表示未按下，持续监听）
isPushed = False

if __name__ == "__main__":


    while not isPushed:
        user_input = listen_and_recognize()
        if user_input:
            print("识别内容：", user_input)
            # 这里可以加入 ChatGPT 回答逻辑，比如使用 GPT-3 给出回复
            # 示例：调用 OpenAI API 获取回复 (这里只是一个占位符)
            response_text = f"你说的是: {user_input}"

            # 朗读返回的文字
            text_to_speech(response_text)
            isPushed = True

        time.sleep(1)  # 控制监听频率

    print("按钮被按下，结束监听")

