#!/usr/bin/env python3
import os
import re
from openai import OpenAI

API_KEY = "fw_3ZLyBejzBgSzRwAADs9vkXFu"
BASE_URL = "https://api.fireworks.ai/inference/v1"
MODEL = "accounts/fireworks/models/qwen3-235b-a22b"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def clean_response(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--/?[^>]*-->\s*", "", text)
    return text.strip()

messages = [{
    "role": "system",
    "content": "Ты — полезный ИИ. Отвечай кратко. НЕ используй <think> или другие технические теги. "
               "Только если пользователь напишет '/think', покажи рассуждения."
}]

print("💬 Чат без <think>. Введите '/think запрос' — чтобы увидеть рассуждения.\n")

try:
    while True:
        user_input = input("Вы: ").strip()
        if not user_input: continue
        if user_input.lower() in ("выход", "exit"): break

        # Команда /think
        if user_input.startswith("/think "):
            query = user_input[len("/think "):]
            temp_msg = [
                {"role": "system", "content": "Покажи рассуждения в <think>...</think>, затем ответ."},
                {"role": "user", "content": query}
            ]
            resp = client.chat.completions.create(model=MODEL, messages=temp_msg, max_tokens=1024)
            print("🧠 (режим рассуждений):")
            print(resp.choices[0].message.content.strip(), "\n")
            continue

        # Обычный запрос
        messages.append({"role": "user", "content": user_input})
        resp = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=512)
        bot_reply = clean_response(resp.choices[0].message.content)
        print("🤖:", bot_reply, "\n")
        messages.append({"role": "assistant", "content": bot_reply})

except KeyboardInterrupt:
    print("\nДо встречи! 🐻")
