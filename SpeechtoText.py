
import openai
import speech_recognition as sr
import pyttsx3
import time

# initialize the engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)
engine.setProperty('rate', 170)


def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please Speak")
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 3
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language='en-UK')
        print("What you said is：", text)
        return text
    except sr.UnknownValueError:
        print("Voice cannot recognize")
        return None
    except sr.RequestError as e:
        print("Error；{0}".format(e))
        return None


def text_to_speech(text):
    if text:
        print(f"Start Reading：{text}")
        engine.say(text)  #
        engine.runAndWait()  # 
    else:
        print("No content to read")


# 模拟按钮状态（False 表示未按下，持续监听）
isPushed = False

if __name__ == "__main__":


    while not isPushed:
        user_input = listen_and_recognize()
        if user_input:
            print("Recognized content：", user_input)
            # 这里可以加入 ChatGPT 回答逻辑，比如使用 GPT-3 给出回复
            # 示例：调用 OpenAI API 获取回复 (这里只是一个占位符)
            response_text = f"What you said is: {user_input}"

            # 朗读返回的文字
            text_to_speech(response_text)
            isPushed = True

        time.sleep(1)  # 控制监听频率

    print("Button is pressed, stopped the program")

