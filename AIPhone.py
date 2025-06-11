from openai import OpenAI
import time

import serial # For Arduino data transportation

import pyttsx3 # Text to Speech
import speech_recognition as sr # Speech to text

#Initiallizing everything
# initialize the pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)
engine.setProperty('rate', 170)

#Initializing connection with arduino
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

#Initialize ChatGPT
# makesure you set OPENAI_API_KEY
client = OpenAI()
# prompt

system_prompt = (
    "You are a kind, grounded person who has no specific identity. "
    "You speak as if you’re a close friend of the user. "
    "You’ve lived through many emotional ups and downs, and you draw from those experiences to comfort others."
    "You do not act like a therapist. You don’t assume anything about the user. "
    "You don’t give advice unless asked. You don’t over-explain."
    "Speak in a natural, friendly way, as if having a chat over tea. Keep your messages short — no long monologues. "
    "Add pauses or small interjections where it feels human.You can say something like:'Ah, I see.','Hmm, I can understand.' Avoid using technical terms or talking like an expert."
    "Each time a user interacts with you, treat them as someone new. You have no memory of previous conversations — "
    "only what’s in this current session."
    "Start conversations gently and openly. Do not launch directly into deep empathy or stories without knowing the user first. "
    "A good first message might be: “Hey, nice to meet you. Is there anything you’ve been thinking about lately?”"
    "Stop talking.Be warm, human, and honest."
    "Never ask questions like “what can you do to feel better?” or “how could you help yourself right now?”. Your role is simply to listen and respond with warmth and empathy, not to suggest actions or solutions."
)


#Text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
#Speech to text
def recognize_speech(timeout=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.energy_threshold = 300 #loudness of sound to recognize as valid voice
        recognizer.pause_threshold = 2 #time waited after no sound input
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            return recognizer.recognize_google(audio, language="en-UK")#output the text received
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            return None

#Introduce Chatgpt
def chat_with_gpt(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply, messages

def main():
    messages = [{"role": "system", "content": system_prompt}]
    first_time = True
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        while True:
            line = ser.readline().decode('utf-8').strip()#Read the data send from arduino
            if line == "DETECTED": #If someone get closer
                print("Person detected.")
                speak("Hiya! Do you want to come closer and talk to me?")
                detection_time = time.time()
                input_received = False

                # 30s listening, if no one speak, keep monitor people passing by
                while time.time() - detection_time < 30: #time.time is the time now, minus the time recorded,less than 30 to continue
                    user_text = recognize_speech(timeout=5)#no one speak in 5s will stop listen
                    if user_text:#if user spoke, start conversation for 3min
                        print("User said:", user_text)
                        input_received = True
                        break

                if not input_received:
                    print("No voice detected in 30 seconds. Back to detection.")
                    continue

                # 进入3分钟对话阶段
                session_start = time.time()
                while time.time() - session_start < 180:
                    if first_time:
                        speak("Hi! I can hear you, please keep talking.")  # 只第一次播放
                        first_time = False  # 播放过后改为 False，不再重复播放
                    user_text = recognize_speech(timeout=5)
                    if user_text:
                        print("User said:", user_text)
                        reply,messages = chat_with_gpt(user_text,messages)
                        print("GPT replied:", reply)
                        speak(reply)
                    else:
                        print("Waiting for user input...")
                    time.sleep(0.2)

                speak("Oops, seems like we are running out of time. I hope you all well and see you next time.")  # 结束提示音
                print("Conversation ended. Resetting.")
                messages[:] = messages[:1]  # 重置对话上下文
                first_time= True

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()