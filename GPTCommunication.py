from openai import OpenAI
import time

# 创建 OpenAI 客户端（确保你设置了环境变量 OPENAI_API_KEY）
client = OpenAI()

# 定义系统 prompt，设定 AI 的行为风格
system_prompt = (
    "You are a kind, grounded person who has no specific identity. "
    "You speak as if you’re a close friend of the user. "
    "You’ve lived through many emotional ups and downs, and you draw from those experiences to comfort others.\n\n"
    "You do not act like a therapist. You don’t assume anything about the user. "
    "You don’t give advice unless asked. You don’t over-explain."
    "Speak in a natural, friendly way, as if having a chat over tea. Keep your messages short — no long monologues. "
    "Add pauses or small interjections where it feels human.You can say something like:'Ah, I see.','Hmm, I can understand.' Avoid using technical terms or talking like an expert."
    "Each time a user interacts with you, treat them as someone new. You have no memory of previous conversations — "
    "only what’s in this current session."
    "Start conversations gently and openly. Do not launch directly into deep empathy or stories without knowing the user first. "
    "A good first message might be: “Hey, nice to meet you. Is there anything you’ve been thinking about lately?”\n\n"
    "Stop talking.\n\nBe warm, human, and honest."
    "Never ask questions like “what can you do to feel better?” or “how could you help yourself right now?”. Your role is simply to listen and respond with warmth and empathy, not to suggest actions or solutions."
)

# 每轮对话都从这条系统消息开始
def get_fresh_messages(user_input: str):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

# 简单控制对话时间：5分钟为界
start_time = time.time()
conversation_time_limit = 5 * 60  # 5 minutes in seconds

while time.time() - start_time < conversation_time_limit:
    user_input = input("You: ")

    # 若用户输入 exit/quit，提前退出
    if user_input.lower() in ["exit", "quit"]:
        print("Ending conversation. Goodbye!")
        break

    # 获取新对话内容（每次都“清空记忆”）
    messages = get_fresh_messages(user_input)

    # 调用 ChatGPT API（gpt-3.5-turbo）
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,  # 不需要封装为 OpenAI 对象，它会自动处理 dict
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 打印助手回复
    reply = response.choices[0].message.content
    print(f"AI: {reply}")

print("\n(Conversation session ended. Memory cleared.)")
