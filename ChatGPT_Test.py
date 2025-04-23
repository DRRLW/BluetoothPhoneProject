import openai
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
client = OpenAI()

# 初始化语音合成引擎
engine = pyttsx3.init()

def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        audio = recognizer.listen(source)
    try:
        print("正在识别...")
        text = recognizer.recognize_google(audio, language='zh-CN')  # 中文识别
        print("你说的是：", text)
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
        return None
    except sr.RequestError as e:
        print("识别服务出错；{0}".format(e))
        return None

'''def ask_chatgpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    print("ChatGPT：", answer)
    return answer

def speak_text(text):
    engine.say(text)
    engine.runAndWait()'''

# 主程序
if __name__ == "__main__":
    user_input = listen_and_recognize()
    print(user_input)
    '''if user_input:
        reply = ask_chatgpt(user_input)
        speak_text(reply)'''

